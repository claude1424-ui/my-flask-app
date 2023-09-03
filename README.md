# My Flask App

This is a simple Flask application that demonstrates how to use Flask with Vercel.

## Getting Started

To run this application locally, follow these steps:

1. Clone this repository.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Run the application using `python app.py`.

## Deploying to Vercel

To deploy this application to Vercel, you can follow these steps:

1. Install the Vercel CLI if you haven't already (`npm install -g vercel`).
2. Log in to your Vercel account using `vercel login`.
3. Create a `vercel.json` configuration file (example provided below).
4. Deploy the application using `vercel --prod`.

## Example `vercel.json`

```json
{
  "version": 2,
  "builds": [{ "src": "app.py", "use": "@vercel/python" }],
  "routes": [
    { "src": "/", "dest": "app.py" },
    { "src": "/(.*)", "dest": "app.py" }
  ]
}

