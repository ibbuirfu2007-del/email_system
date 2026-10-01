"""
Email Management System

A simple object-oriented email management system
with inbox, email status, search, delete, and forwarding features.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import uuid4


class EmailStatus(Enum):
    """Represents the current status of an email."""

    READ = "Read"
    UNREAD = "Unread"


@dataclass
class Email:
    """Represents an email message."""

    sender: "User"
    receiver: "User"
    subject: str
    body: str

    email_id: str = field(default_factory=lambda: str(uuid4())[:8])
    timestamp: datetime = field(default_factory=datetime.now)
    status: EmailStatus = EmailStatus.UNREAD

    def mark_as_read(self) -> None:
        """Mark the email as read."""
        self.status = EmailStatus.READ

    def mark_as_unread(self) -> None:
        """Mark the email as unread."""
        self.status = EmailStatus.UNREAD

    def display(self) -> None:
        """Display the complete email."""

        self.mark_as_read()

        print("\n" + "=" * 50)
        print("EMAIL DETAILS")
        print("=" * 50)
        print(f"Email ID : {self.email_id}")
        print(f"From     : {self.sender.name}")
        print(f"To       : {self.receiver.name}")
        print(f"Subject  : {self.subject}")
        print(
            f"Received : "
            f"{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
        )
        print(f"Status   : {self.status.value}")
        print("-" * 50)
        print(f"Body     : {self.body}")
        print("=" * 50)

    def __str__(self) -> str:
        """Return a short email summary."""

        return (
            f"[{self.status.value}] "
            f"{self.sender.name} | "
            f"{self.subject} | "
            f"{self.timestamp.strftime('%Y-%m-%d %H:%M')}"
        )


class Inbox:
    """Manages emails received by a user."""

    def __init__(self) -> None:
        self.emails: List[Email] = []

    def receive_email(self, email: Email) -> None:
        """Add an email to the inbox."""

        self.emails.append(email)

    def list_emails(self) -> None:
        """Display all emails in the inbox."""

        if not self.emails:
            print("\nInbox is empty.")
            return

        print("\n" + "=" * 60)
        print("INBOX")
        print("=" * 60)

        for index, email in enumerate(self.emails, start=1):
            print(f"{index}. {email}")

        print("=" * 60)

    def get_email(self, index: int) -> Optional[Email]:
        """Return an email using its inbox position."""

        if index < 1 or index > len(self.emails):
            return None

        return self.emails[index - 1]

    def read_email(self, index: int) -> None:
        """Read an email from the inbox."""

        email = self.get_email(index)

        if email is None:
            print("\nInvalid email number.")
            return

        email.display()

    def delete_email(self, index: int) -> None:
        """Delete an email from the inbox."""

        email = self.get_email(index)

        if email is None:
            print("\nInvalid email number.")
            return

        self.emails.remove(email)
        print(f"\nEmail '{email.subject}' deleted successfully.")

    def search(self, keyword: str) -> List[Email]:
        """Search emails by sender or subject."""

        keyword = keyword.lower()

        return [
            email
            for email in self.emails
            if keyword in email.subject.lower()
            or keyword in email.sender.name.lower()
        ]

    def unread_count(self) -> int:
        """Return the number of unread emails."""

        return sum(
            email.status == EmailStatus.UNREAD
            for email in self.emails
        )

    def mark_all_as_read(self) -> None:
        """Mark every email as read."""

        for email in self.emails:
            email.mark_as_read()

        print("\nAll emails marked as read.")

    def statistics(self) -> None:
        """Display inbox statistics."""

        total = len(self.emails)
        unread = self.unread_count()
        read = total - unread

        print("\n" + "=" * 40)
        print("INBOX STATISTICS")
        print("=" * 40)
        print(f"Total Emails   : {total}")
        print(f"Read Emails    : {read}")
        print(f"Unread Emails  : {unread}")
        print("=" * 40)


class User:
    """Represents an email system user."""

    def __init__(self, name: str, email_address: str) -> None:
        self.name = name
        self.email_address = email_address
        self.inbox = Inbox()

    def send_email(
        self,
        receiver: "User",
        subject: str,
        body: str
    ) -> Email:
        """Create and send an email."""

        email = Email(
            sender=self,
            receiver=receiver,
            subject=subject,
            body=body
        )

        receiver.inbox.receive_email(email)

        print(
            f"\nEmail sent successfully: "
            f"{self.name} → {receiver.name}"
        )

        return email

    def forward_email(
        self,
        email: Email,
        receiver: "User"
    ) -> Email:
        """Forward an existing email to another user."""

        forwarded_body = (
            f"---------- Forwarded Email ----------\n"
            f"From: {email.sender.email_address}\n"
            f"Subject: {email.subject}\n\n"
            f"{email.body}"
        )

        return self.send_email(
            receiver,
            f"Fwd: {email.subject}",
            forwarded_body
        )

    def check_inbox(self) -> None:
        """Display the user's inbox."""

        print(f"\n{self.name}'s Inbox")
        self.inbox.list_emails()


def main() -> None:
    """Run the email management system."""

    # Create users
    tory = User("Tory", "tory@example.com")
    ramy = User("Ramy", "ramy@example.com")
    alex = User("Alex", "alex@example.com")

    # Send emails
    tory.send_email(
        ramy,
        "Welcome",
        "Hi Ramy, welcome to our email system!"
    )

    ramy.send_email(
        tory,
        "Re: Welcome",
        "Hi Tory, thank you for the message."
    )

    tory.send_email(
        ramy,
        "Project Update",
        "The project has been completed successfully."
    )

    # Display inbox
    ramy.check_inbox()

    # Read first email
    ramy.inbox.read_email(1)

    # Display statistics
    ramy.inbox.statistics()

    # Search emails
    print("\nSearch Results:")
    results = ramy.inbox.search("project")

    for email in results:
        print(email)

    # Forward email
    if results:
        ramy.forward_email(results[0], alex)

    # Delete an email
    ramy.inbox.delete_email(2)

    # Final inbox
    ramy.check_inbox()


if __name__ == "__main__":
    main()