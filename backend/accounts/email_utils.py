"""
Email utilities for sending emails using Resend
"""
import resend
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from decouple import config
import logging

logger = logging.getLogger(__name__)

# Initialize Resend with API key
resend.api_key = config('RESEND_API_KEY', default='re_demo_key')


class EmailService:
    """Service class for handling email operations"""

    @staticmethod
    def send_email(to_email, subject, template_name, context=None):
        """
        Send an email using Resend

        Args:
            to_email: Recipient email address
            subject: Email subject
            template_name: Name of the email template
            context: Context dictionary for template rendering

        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            # Add default context
            default_context = {
                'site_name': config('SITE_NAME', default='Bloomvest Capital'),
                'site_url': config('SITE_URL', default='http://localhost:8000'),
                'support_email': 'support@bloomvestcapital.com',
            }

            if context:
                default_context.update(context)

            # Render email templates
            html_content = render_to_string(f'emails/{template_name}.html', default_context)
            text_content = strip_tags(html_content)

            # Log email attempt
            logger.info(f"Attempting to send '{subject}' email to {to_email}")

            # Send email using Resend
            response = resend.Emails.send({
                "from": f"{config('EMAIL_FROM_NAME', default='Bloomvest Capital')} <{config('EMAIL_FROM', default='onboarding@resend.dev')}>",
                "to": to_email,
                "subject": subject,
                "html": html_content,
                "text": text_content
            })

            logger.info(f"✅ Email sent successfully to {to_email} | Subject: {subject} | Response: {response}")
            print(f"\n{'='*80}")
            print(f"✅ EMAIL SENT SUCCESSFULLY")
            print(f"{'='*80}")
            print(f"To: {to_email}")
            print(f"Subject: {subject}")
            print(f"Template: {template_name}")
            print(f"Response: {response}")
            print(f"{'='*80}\n")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to send email to {to_email}: {str(e)}")
            print(f"\n{'='*80}")
            print(f"❌ EMAIL FAILED")
            print(f"{'='*80}")
            print(f"To: {to_email}")
            print(f"Subject: {subject}")
            print(f"Error: {str(e)}")
            print(f"{'='*80}\n")
            # In demo mode, we'll return False to show the error
            return False

    @staticmethod
    def send_verification_email(user, verification_token):
        """Send email verification link to user"""
        context = {
            'user': user,
            'verification_link': f"{config('SITE_URL')}/auth/verify-email/{verification_token}/",
            'username': user.username,
            'first_name': user.first_name or user.username,
        }

        return EmailService.send_email(
            to_email=user.email,
            subject='Verify Your Email - Bloomvest Capital',
            template_name='verification_email',
            context=context
        )

    @staticmethod
    def send_welcome_email(user):
        """Send welcome email to new user"""
        context = {
            'user': user,
            'username': user.username,
            'first_name': user.first_name or user.username,
            'dashboard_url': f"{config('SITE_URL')}/dashboard/",
        }

        return EmailService.send_email(
            to_email=user.email,
            subject='Welcome to Bloomvest Capital',
            template_name='welcome_email',
            context=context
        )

    @staticmethod
    def send_password_reset_email(user, reset_token):
        """Send password reset email to user"""
        context = {
            'user': user,
            'reset_link': f"{config('SITE_URL')}/auth/reset-password/{reset_token}/",
            'username': user.username,
            'first_name': user.first_name or user.username,
        }

        return EmailService.send_email(
            to_email=user.email,
            subject='Reset Your Password - Bloomvest Capital',
            template_name='password_reset_email',
            context=context
        )

    @staticmethod
    def send_login_alert_email(user, ip_address=None, user_agent=None):
        """Send login alert email to user"""
        context = {
            'user': user,
            'username': user.username,
            'first_name': user.first_name or user.username,
            'ip_address': ip_address or 'Unknown',
            'user_agent': user_agent or 'Unknown',
        }

        return EmailService.send_email(
            to_email=user.email,
            subject='New Login to Your Account - Bloomvest Capital',
            template_name='login_alert_email',
            context=context
        )