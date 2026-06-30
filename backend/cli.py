from jacob_core.core import JacobCore
from jacob_core.models import PartnerMessage


def main() -> None:
    print("Jacob Core 0.1")
    print("Digite 'sair' para encerrar.\n")

    core = JacobCore()
    partner_name = "Jason"

    while True:
        content = input(f"{partner_name}: ").strip()
        if content.lower() in {"sair", "exit", "quit"}:
            print("Jacob: Até logo, parceiro.")
            break

        response = core.handle(PartnerMessage(partner_name=partner_name, content=content))
        print(f"\nJacob ({response.specialist_name}):")
        print(response.text)
        print("\n--- debug ---")
        print(f"intent: {response.intent.value}")
        print(f"reflection: {response.reflection.notes}")
        print("-------------\n")


if __name__ == "__main__":
    main()
