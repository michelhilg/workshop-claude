import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import google.auth.exceptions
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / ".claude" / "agents" / "extrator" / "config.json"


def load_config():
    with open(CONFIG_PATH, encoding="utf-8") as f:
        cfg = json.load(f)
    cfg["credentials_path"] = PROJECT_ROOT / cfg["credentials_path"]
    cfg["output_dir"] = PROJECT_ROOT / cfg["output_dir"]
    return cfg


def build_service(credentials_path):
    creds = service_account.Credentials.from_service_account_file(
        str(credentials_path), scopes=SCOPES
    )
    return build("sheets", "v4", credentials=creds)


def get_first_tab(service, spreadsheet_id):
    meta = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    return meta["sheets"][0]["properties"]["title"]


def extract_sheet(service, sheet_cfg, extracted_at):
    spreadsheet_id = sheet_cfg["spreadsheet_id"]
    name = sheet_cfg["name"]
    tab = sheet_cfg["tab"]

    try:
        result = (
            service.spreadsheets()
            .values()
            .get(spreadsheetId=spreadsheet_id, range=tab)
            .execute()
        )
    except HttpError as e:
        if e.resp.status in (400, 404):
            tab = get_first_tab(service, spreadsheet_id)
            result = (
                service.spreadsheets()
                .values()
                .get(spreadsheetId=spreadsheet_id, range=tab)
                .execute()
            )
        else:
            raise

    rows = result.get("values", [])
    if not rows:
        return []

    headers = rows[0]
    records = []
    for row in rows[1:]:
        padded = row + [""] * (len(headers) - len(row))
        record = dict(zip(headers, padded))
        record["_source_sheet"] = name
        record["_extracted_at"] = extracted_at
        records.append(record)

    return records


def main():
    try:
        config = load_config()
    except FileNotFoundError:
        print(f"ERRO: config.json não encontrado em {CONFIG_PATH}", file=sys.stderr)
        sys.exit(1)

    output_dir = config["output_dir"]
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        service = build_service(config["credentials_path"])
    except google.auth.exceptions.GoogleAuthError as e:
        print(
            f"ERRO DE AUTENTICAÇÃO: {e}\n"
            "O token de autenticação pode ter expirado. "
            "Verifique o arquivo service_account.json em .claude/agents/extrator/",
            file=sys.stderr,
        )
        sys.exit(1)
    except FileNotFoundError:
        print(
            "ERRO: Arquivo de credenciais não encontrado.\n"
            f"Coloque o service_account.json em: {config['credentials_path']}",
            file=sys.stderr,
        )
        sys.exit(1)

    extracted_at = datetime.now(timezone.utc).isoformat()
    manifest = {"extracted_at": extracted_at, "sources": {}}
    total_failures = 0

    print(f"\nExtração iniciada em {extracted_at}\n{'─' * 50}")

    for sheet_cfg in config["sheets"]:
        name = sheet_cfg["name"]
        try:
            records = extract_sheet(service, sheet_cfg, extracted_at)
            out_path = output_dir / f"{name}.json"
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(records, f, ensure_ascii=False, indent=2)
            manifest["sources"][name] = {
                "status": "success",
                "record_count": len(records),
                "output_file": str(out_path.relative_to(PROJECT_ROOT)),
            }
            print(f"  ✓ {name:<20} — {len(records):>6} registros")
        except google.auth.exceptions.GoogleAuthError as e:
            total_failures += 1
            manifest["sources"][name] = {"status": "auth_error", "error": str(e)}
            print(
                f"  ✗ {name:<20} — ERRO DE AUTENTICAÇÃO: token pode ter expirado",
                file=sys.stderr,
            )
        except Exception as e:
            total_failures += 1
            manifest["sources"][name] = {"status": "error", "error": str(e)}
            print(f"  ✗ {name:<20} — FALHA: {e}", file=sys.stderr)

    manifest_path = output_dir / "extraction_manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"{'─' * 50}")
    print(f"extraction_manifest.json salvo em {manifest_path.relative_to(PROJECT_ROOT)}")

    if total_failures == len(config["sheets"]):
        print("\nFALHA TOTAL: todas as planilhas falharam.", file=sys.stderr)
        sys.exit(1)

    if total_failures > 0:
        print(f"\nExtração concluída com {total_failures} falha(s) parcial(is).")
    else:
        print("\nExtração concluída com sucesso.")


if __name__ == "__main__":
    main()
