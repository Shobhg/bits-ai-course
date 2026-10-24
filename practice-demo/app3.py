from pathlib import Path

from services.json_service import(
    generate_structured_response
)


def main():

    text_file = Path("long_text.txt")

    text = text_file.read_text(encoding="utf-8")



    try:

        result = generate_structured_response(text)

        print("\n-------------RESULT---------")
        print (result)

        print("\n-------------SUMMARY---------")

        print(result.summary)


        print("\n-------------KEYWORDS---------")
        
        for keyword in result.keywords:
            print("-", keyword)

        print("\n-------------JSON---------")

        print(result.model_dump_json(indent = 2))

    except Exception as e:
        print(f"Unexpected error: {e} ")



if __name__ == "__main__":
    main()