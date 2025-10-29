#!/usr/bin/env python3
"""
CLI simples para consumir a API do projeto.
Comandos:
  list                - listar projetos
  detail <id>         - mostrar detalhe do projeto
  create              - criar projeto (nome, descricao)
  register            - cadastrar usuário
  login               - autenticar e salvar token

O token JWT é salvo em `.token` na raiz do projeto.
"""

import argparse
import json
import os
import sys
from typing import Optional

import requests

BASE = os.environ.get("API_BASE", "http://localhost:8000/api")
TOKEN_FILE = ".token"


def save_token(token: str):
    with open(TOKEN_FILE, "w") as f:
        f.write(token)


def load_token() -> Optional[str]:
    if not os.path.exists(TOKEN_FILE):
        return None
    with open(TOKEN_FILE) as f:
        return f.read().strip()


def auth_headers():
    token = load_token()
    if not token:
        return {}
    return {"Authorization": f"Bearer {token}"}


def cmd_list(args):
    url = f"{BASE}/projeto/"
    r = requests.get(url)
    r.raise_for_status()
    data = r.json()
    for item in data:
        print(f"{item['id']}: {item.get('nome')} - {item.get('descricao')}")


def cmd_detail(args):
    url = f"{BASE}/projeto/{args.id}/"
    r = requests.get(url)
    if r.status_code == 404:
        print("Projeto não encontrado")
        return
    r.raise_for_status()
    data = r.json()
    print(json.dumps(data, indent=2, ensure_ascii=False))


def cmd_create(args):
    url = f"{BASE}/projeto/"
    payload = {"nome": args.nome, "descricao": args.descricao}
    headers = {"Content-Type": "application/json"}
    headers.update(auth_headers())
    r = requests.post(url, json=payload, headers=headers)
    if r.status_code in (200, 201):
        print("Projeto criado:")
        print(json.dumps(r.json(), indent=2, ensure_ascii=False))
    else:
        print("Erro ao criar projeto", r.status_code)
        try:
            print(r.json())
        except Exception:
            print(r.text)


def cmd_tarefa(args):
    url = f"{BASE}/projeto/{args.id}/criar-tarefa/"
    payload = {"nome": args.nome, "descricao": args.descricao}
    headers = {"Content-Type": "application/json"}
    headers.update(auth_headers())
    r = requests.post(url, json=payload, headers=headers)
    if r.status_code in (200, 201):
        print("Tarefa criada:")
        print(json.dumps(r.json(), indent=2, ensure_ascii=False))
    else:
        print("Erro ao criar tarefa", r.status_code)
        try:
            print(r.json())
        except Exception:
            print(r.text)


def cmd_register(args):
    url = f"{BASE}/usuario/cadastro/"
    payload = {
        "username": args.username,
        "password": args.password,
        "email": args.email,
    }
    r = requests.post(url, json=payload)
    if r.status_code in (200, 201):
        print("Usuário cadastrado")
        print(r.json())
    else:
        print("Erro ao cadastrar usuário", r.status_code)
        try:
            print(r.json())
        except Exception:
            print(r.text)


def cmd_login(args):
    url = f"{BASE}/usuario/login/"
    payload = {"username": args.username, "password": args.password}
    r = requests.post(url, json=payload)
    if r.status_code != 200:
        print("Falha ao autenticar", r.status_code)
        try:
            print(r.json())
        except Exception:
            print(r.text)
        return
    data = r.json()
    token = data.get("access")
    if not token:
        print("Token não recebido")
        print(data)
        return
    save_token(token)
    print("Token salvo em .token")


def main():
    parser = argparse.ArgumentParser(description="CLI para API de Projeto")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("list", help="Listar projetos")

    pd = sub.add_parser("detail", help="Detalhe de um projeto")
    pd.add_argument("id", type=int)

    pc = sub.add_parser("create", help="Criar projeto")
    pc.add_argument("--nome", required=True)
    pc.add_argument("--descricao", required=True)

    pt = sub.add_parser("tarefa", help="Criar tarefa em um projeto")
    pt.add_argument("id", type=int, help="ID do projeto")
    pt.add_argument("--nome", required=True, help="Nome da tarefa")
    pt.add_argument("--descricao", required=True, help="Descrição da tarefa")

    pr = sub.add_parser("register", help="Cadastrar usuário")
    pr.add_argument("--username", required=True)
    pr.add_argument("--password", required=True)
    pr.add_argument("--email", default="")

    pl = sub.add_parser("login", help="Login e salvar token")
    pl.add_argument("--username", required=True)
    pl.add_argument("--password", required=True)

    args = parser.parse_args()
    if not args.cmd:
        parser.print_help()
        sys.exit(1)

    try:
        if args.cmd == "list":
            cmd_list(args)
        elif args.cmd == "detail":
            cmd_detail(args)
        elif args.cmd == "create":
            cmd_create(args)
        elif args.cmd == "tarefa":
            cmd_tarefa(args)
        elif args.cmd == "register":
            cmd_register(args)
        elif args.cmd == "login":
            cmd_login(args)
    except requests.exceptions.ConnectionError:
        print(
            'Não foi possível conectar com o servidor. Execute "python manage.py runserver" no projeto ou ajuste a variável de ambiente API_BASE.'
        )
    except requests.HTTPError as e:
        print("HTTP error:", e)


if __name__ == "__main__":
    main()
