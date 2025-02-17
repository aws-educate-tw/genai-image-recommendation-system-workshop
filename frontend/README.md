# Frontend Setup for AWS Generative AI Hackathon Project

This README provides instructions on how to set up and run the frontend for the AWS Generative AI Hackathon project.

## Prerequisites

Ensure you have the following installed:

- Node.js (Latest LTS version recommended)
- npm (Comes with Node.js)

## Installation

Install dependencies:

```bash
npm install
```

## Configuration

Set up environment variables for API access:

```bash
echo "VITE_API_URL=<API_URL>" > .env.development
```

Replace `<API_URL>` with the actual backend API endpoint.

## Running the Application

Start the development server:

```bash
npm run dev
```

This will launch the frontend at `http://localhost:5173/` (or another port if 5173 is in use). Open this URL in your browser to access the application.
