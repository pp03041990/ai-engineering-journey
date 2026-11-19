# Booking API Troubleshooting Guide

## HTTP 404 - Not Found

Possible causes:

- Booking ID does not exist.
- Incorrect endpoint or environment.
- Booking lookup mapping is incorrect.

## HTTP 503 - Service Unavailable

Possible causes:

- Backend service is unavailable.
- Database connectivity issues.
- Upstream service timeout.

## QA Investigation Checklist

1. Verify the request URL and booking ID.
2. Check expected versus actual HTTP status.
3. Confirm the test data exists.
4. Review application logs.
5. Compare with historical incidents.
