// frontend/src/services/api.js

export const startScraping = async (url) => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/test-scrape-users/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ url: url })
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    console.log("Started scraping users...");
    return response.json();
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
};

export const startScraper = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/start-scraper/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    console.log("Started backend scraper...");
    return response.json();
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
};

export const pauseScraping = async (usernames) => {
  const response = await fetch('http://127.0.0.1:8000/api/pause/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ usernames })
  });

  if (!response.ok) {
    throw new Error('Network response was not ok');
  }

  return response.json();
};

export const downloadExcel = async () => {
  const response = await fetch('http://127.0.0.1:8000/api/download-excel/');
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }

  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'demo_excel_file.xlsx';
  document.body.appendChild(a);
  a.click();
  a.remove();
};
