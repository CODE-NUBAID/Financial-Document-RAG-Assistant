from rag_utils import load_pdf, split_documents, create_vector_db, answer_query

PDF_PATH = "invoice.pdf"

def main():
    print("📄 Loading invoice...")

    try:
        docs = load_pdf(PDF_PATH)
    except Exception as e:
        print(e)
        return

    print("✂️ Splitting document...")
    split_docs = split_documents(docs)

    print("🧠 Creating vector database...")
    db = create_vector_db(split_docs)

    print("\n✅ System Ready! Ask questions (type 'exit' to quit)\n")

    while True:
        query = input("❓ Your Question: ")

        if query.lower() == "exit":
            print("👋 Exiting...")
            break

        try:
            answer, source_docs = answer_query(db, query)

            print("\n🤖 Answer:")
            print(answer)

            print("\n📌 Retrieved Context Preview:")
            for i, doc in enumerate(source_docs[:2]):
                print(f"\n--- Chunk {i+1} ---\n{doc.page_content[:200]}...")

            print("\n" + "="*50 + "\n")

        except Exception as e:
            print("❌ Error:", e)


if __name__ == "__main__":
    main()
