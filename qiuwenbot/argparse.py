from typing import List

from dargs import Argument, Variant


def page_variant() -> Variant:
    doc_type = "Method to scan pages."
    doc_type_all = "Scan all pages in alphabetical order."
    doc_type_new = "Scan new pages."
    doc_type_link = "Scan pages that link to a page or include a template."
    doc_type_page = "Scan a single page."
    doc_link_name = "Name of the page or template."
    doc_namespace = "Namespace(s) of the pages."
    doc_start = "Start time in ISO format."
    doc_end = "End time in ISO format."
    doc_restart = "Restart from the last page in the log."

    return Variant(
        "type",
        [
            Argument(
                "all",
                dtype=dict,
                sub_fields=[
                    Argument(
                        "namespace",
                        dtype=int,
                        optional=True,
                        default=0,
                        doc=doc_namespace,
                    ),
                    Argument(
                        "restart",
                        dtype=bool,
                        optional=True,
                        default=False,
                        doc=doc_restart,
                    ),
                ],
                doc=doc_type_all,
            ),
            Argument(
                "new",
                dtype=dict,
                sub_fields=[
                    Argument(
                        "namespace",
                        dtype=[int, list],
                        optional=True,
                        default=0,
                        doc=doc_namespace,
                    ),
                    Argument(
                        "start", dtype=str, optional=True, default=None, doc=doc_start
                    ),
                    Argument(
                        "end", dtype=str, optional=True, default=None, doc=doc_end
                    ),
                ],
                doc=doc_type_new,
            ),
            Argument(
                "link",
                dtype=dict,
                sub_fields=[
                    Argument("name", dtype=str, doc=doc_link_name),
                    Argument(
                        "namespace",
                        dtype=[int, list],
                        optional=True,
                        default=None,
                        doc=doc_namespace,
                    ),
                ],
                alias=["template"],
                doc=doc_type_link,
            ),
            Argument(
                "page",
                dtype=dict,
                sub_fields=[
                    Argument("name", dtype=str, doc=doc_link_name),
                ],
                doc=doc_type_page,
            ),
        ],
        doc=doc_type,
    )


def submit_args() -> List[Argument]:
    doc_user = "Username."
    doc_pages = "Configurations of scanned pages."
    doc_task = "Task to submit."
    return [
        Argument("user", dtype=str, doc=doc_user),
        Argument("pages", dtype=dict, doc=doc_pages, sub_variants=[page_variant()]),
        Argument("task", dtype=str, doc=doc_task),
    ]


def normalize(data: dict) -> dict:
    base = Argument("base", dtype=dict, sub_fields=submit_args())
    base.check_value(data, strict=True)
    return base.normalize(data)
