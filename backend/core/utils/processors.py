import hashlib
from models.brains import Brain
from models.files import File
from models.data import Data
from models.settings import get_supabase_db
from parsers.common import process_data
from parsers.audio import process_audio
from parsers.csv import process_csv
from parsers.docx import process_docx
from parsers.epub import process_epub
from parsers.html import process_html
from parsers.markdown import process_markdown
from parsers.notebook import process_ipnyb
from parsers.odt import process_odt
from parsers.pdf import process_pdf
from parsers.powerpoint import process_powerpoint
from parsers.txt import process_txt

file_processors = {
    ".txt": process_txt,
    ".csv": process_csv,
    ".md": process_markdown,
    ".markdown": process_markdown,
    ".m4a": process_audio,
    ".mp3": process_audio,
    ".webm": process_audio,
    ".mp4": process_audio,
    ".mpga": process_audio,
    ".wav": process_audio,
    ".mpeg": process_audio,
    ".pdf": process_pdf,
    ".html": process_html,
    ".pptx": process_powerpoint,
    ".docx": process_docx,
    ".odt": process_odt,
    ".epub": process_epub,
    ".ipynb": process_ipnyb,
}


def create_response(message, type):
    return {"message": message, "type": type}


async def filter_file(
    file: File,
    enable_summarization: bool,
    brain_id,
    openai_api_key,
):
    await file.compute_file_sha1()

    print("file sha1", file.file_sha1)
    # file_exists = file.file_already_exists()
    file_exists_in_brain = file.file_already_exists_in_brain(brain_id)

    if file_exists_in_brain:
        return create_response(
            f"🤔 {file.file.filename} already exists in brain {brain_id}.",  # pyright: ignore reportPrivateUsage=none
            "warning",
        )
    elif file.file_is_empty():
        return create_response(
            f"❌ {file.file.filename} is empty.",  # pyright: ignore reportPrivateUsage=none
            "error",  # pyright: ignore reportPrivateUsage=none
        )
    # elif file_exists:
    #     file.link_file_to_brain(brain=Brain(id=brain_id))
    #     return create_response(
    #         f"✅ {file.file.filename} has been uploaded to brain {brain_id}.",  # pyright: ignore reportPrivateUsage=none
    #         "success",
    #     )

    if file.file_extension in file_processors:
        try:
            await file_processors[file.file_extension](
                file=file,
                enable_summarization=enable_summarization,
                brain_id=brain_id,
                user_openai_api_key=openai_api_key,
            )
            return create_response(
                f"✅ {file.file.filename} has been uploaded to brain {brain_id}.",  # pyright: ignore reportPrivateUsage=none
                "success",
            )
        except Exception as e:
            # Add more specific exceptions as needed.
            print(f"Error processing file: {e}")
            return create_response(
                f"⚠️ An error occurred while processing {file.file.filename}.",  # pyright: ignore reportPrivateUsage=none
                "error",
            )

    return create_response(
        f"❌ {file.file.filename} is not supported.",  # pyright: ignore reportPrivateUsage=none
        "error",
    )

async def filter_data(
    data: Data,
    brain_id,
):
    await data.compute_data_sha1()

    print("data sha1", data.data_sha1)
    # data_exists = data.data_already_exists()
    data_exists_in_brain = data.data_already_exists_in_brain(brain_id)

    if data_exists_in_brain:
        return create_response(
            f"🤔 data already exists in brain {brain_id}.",  # pyright: ignore reportPrivateUsage=none
            "warning",
        )
    elif data.data_is_empty():
        return create_response(
            f"❌ data is empty.",  # pyright: ignore reportPrivateUsage=none
            "error",  # pyright: ignore reportPrivateUsage=none
        )
    # elif data_exists:
    #     data.link_data_to_brain(brain=Brain(id=brain_id))
    #     return create_response(
    #         f"✅ data has been uploaded to brain {brain_id}.",  # pyright: ignore reportPrivateUsage=none
    #         "success",
    #     )

    try:
        await process_data(
            data=data,
            brain_id=brain_id,
        )
        return create_response(
            f"✅ data has been uploaded to brain {brain_id}.",  # pyright: ignore reportPrivateUsage=none
            "success",
        )
    except Exception as e:
        # Add more specific exceptions as needed.
        print(f"Error processing file: {e}")
        return create_response(
            f"⚠️ An error occurred while processing",  # pyright: ignore reportPrivateUsage=none
            "error",
        )

    # return create_response(
    #     f"❌ {file.file.filename} is not supported.",  # pyright: ignore reportPrivateUsage=none
    #     "error",
    # )
    # data_sha1 = hashlib.sha1(data).hexdigest()

    # print("data sha1", data_sha1)

    # supabase_db = get_supabase_db()
    # # already exist
    # vectors_ids = supabase_db.get_brain_vectors_by_brain_id_and_file_sha1(brain_id, data_sha1).data
    # if len(vectors_ids) == 0:
    #     return create_response(
    #         f"🤔 already exists in brain {brain_id}.",  # pyright: ignore reportPrivateUsage=none
    #         "warning",
    #     )
    # elif data == "":
    #     return create_response(
    #         f"❌ data is empty.",  # pyright: ignore reportPrivateUsage=none
    #         "error",  # pyright: ignore reportPrivateUsage=none
    #     )
    # else:
    #     vectors_ids = supabase_db.get_vectors_by_file_sha1(data_sha1).data
    #     file.link_file_to_brain(brain=Brain(id=brain_id))
    #     return create_response(
    #         f"✅ {file.file.filename} has been uploaded to brain {brain_id}.",  # pyright: ignore reportPrivateUsage=none
    #         "success",
    #     )

    # if file.file_extension in file_processors:
    #     try:
    #         await file_processors[file.file_extension](
    #             file=file,
    #             enable_summarization=enable_summarization,
    #             brain_id=brain_id,
    #             user_openai_api_key=openai_api_key,
    #         )
    #         return create_response(
    #             f"✅ {file.file.filename} has been uploaded to brain {brain_id}.",  # pyright: ignore reportPrivateUsage=none
    #             "success",
    #         )
    #     except Exception as e:
    #         # Add more specific exceptions as needed.
    #         print(f"Error processing file: {e}")
    #         return create_response(
    #             f"⚠️ An error occurred while processing {file.file.filename}.",  # pyright: ignore reportPrivateUsage=none
    #             "error",
    #         )

    # return create_response(
    #     f"❌ {file.file.filename} is not supported.",  # pyright: ignore reportPrivateUsage=none
    #     "error",
    # )
    