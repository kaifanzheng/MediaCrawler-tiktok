export const fetchRandomText = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/random-text/', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      });
  
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
  
      const data = await response.json();
      return data.text;
    } catch (error) {
      console.error('Error fetching random text:', error);
      throw error;
    }
  };
  