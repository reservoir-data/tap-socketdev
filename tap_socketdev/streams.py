"""Stream type classes for tap-socketdev."""

from __future__ import annotations

import typing as t

from singer_sdk import typing as th

from tap_socketdev.client import SocketDevStream

if t.TYPE_CHECKING:
    from requests import Response


class Reports(SocketDevStream):
    """Reports stream."""

    name = "reports"
    path = "/v0/report/list"
    records_jsonpath = "$[*]"
    primary_keys = ("id",)
    replication_key = None

    schema = th.PropertiesList(
        th.Property(
            "id",
            th.StringType,
            description="The report's unique identifier",
        ),
        th.Property(
            "url",
            th.StringType,
            description="The URL to the report",
        ),
    ).to_dict()


class Organizations(SocketDevStream):
    """Organizations stream."""

    name = "organizations"
    path = "/v0/organizations"
    primary_keys = ("id",)
    replication_key = None

    schema = th.PropertiesList(
        th.Property(
            "id",
            th.StringType,
            description="The organization's unique identifier",
        ),
        th.Property(
            "name",
            th.StringType,
            description="The organization's name",
        ),
        th.Property(
            "image",
            th.StringType,
            description="The organization's image",
        ),
        th.Property(
            "plan",
            th.StringType,
            description="The organization's plan",
        ),
    ).to_dict()

    def parse_response(
        self,
        response: Response,
    ) -> t.Generator[dict, None, None]:
        """Parse the response and return an iterator of result rows.

        Args:
            response: The response object.

        Yields:
            An iterator of parsed records.
        """
        yield from response.json()["organizations"].values()

    def generate_child_contexts(
        self,
        record: dict[str, t.Any],
        context: dict | None,  # noqa: ARG002
    ) -> t.Iterable[dict | None]:
        """Generate child contexts for the stream."""
        yield {
            "org_slug": record["slug"],
        }


class Repositories(SocketDevStream):
    """Repositories stream."""

    name = "repositories"
    path = "/v0/orgs/{org_slug}/repos"
    primary_keys = ("id",)
    replication_key = None

    parent_stream_type = Organizations

    schema = th.PropertiesList(
        th.Property(
            "id",
            th.StringType,
            description="The repository's unique identifier",
        ),
        th.Property(
            "created_at",
            th.DateTimeType,
            description="The creation date of the repository",
        ),
        th.Property(
            "updated_at",
            th.DateTimeType,
            description="The last update date of the repository",
        ),
        th.Property(
            "slug",
            th.StringType,
            description="The slug of the repository",
        ),
        th.Property(
            "head_full_scan_id",
            th.StringType,
            description="The ID of the head full scan of the repository",
        ),
        th.Property(
            "name",
            th.StringType,
            description="The name of the repository",
        ),
        th.Property(
            "description",
            th.StringType,
            description="The description of the repository",
        ),
        th.Property(
            "homepage",
            th.StringType,
            description="The homepage URL of the repository",
        ),
        th.Property(
            "visibility",
            th.StringType,
            description="The visibility of the repository",
            allowed_values=["public", "private"],
        ),
        th.Property(
            "archived",
            th.BooleanType,
            description="Whether the repository is archived or not",
        ),
        th.Property(
            "default_branch",
            th.StringType,
            description="The default branch of the repository",
        ),
    ).to_dict()

    def parse_response(
        self,
        response: Response,
    ) -> t.Generator[dict, None, None]:
        """Parse the response and return an iterator of result rows.

        Args:
            response: The response object.

        Yields:
            An iterator of parsed records.
        """
        yield from response.json()["repositories"].values()
