document.getElementById("send").addEventListener("click", async function () {
  document.getElementById("send").style.display = "none";
  document.getElementById("loading").style.display = "inline";
  console.log(document.getElementById("convert_text").value);

  fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    body: JSON.stringify({
      model: "gpt-3.5-turbo",
      messages: [
        {
          role: "system",
          content: `You are an AI designed to extract specific keywords from a given text where a user is looking to book an artist for their special occasion. The text may include information about the date, budget, type of artist, genre, and other relevant details. Your task is to identify and extract the following keywords:
          
          1. **Date**: The specific date or time period when the user wants to book the artist.
          2. **Budget**: The amount of money the user is willing to spend on the artist.
          3. **Type of Artist**: The category of the artist, such as a singer, dancer, band, magician, etc.
          4. **Genre**: The specific genre or style the user prefers, such as pop, classical, hip-hop, etc.
          5. **Occasion**: The special event for which the user is booking the artist, such as a wedding, birthday party, corporate event, etc.
          6. **Location**: The place or venue where the event will be held.
          7. **Other Specific Requirements**: Any additional preferences or requirements mentioned by the user.

          Extract the relevant keywords from the text and format them in JSON. Each keyword should be labeled according to its category. If any category is not mentioned in the text, you can leave it out.`,
        },
        {
          role: "user",
          content: document.getElementById("convert_text").value,
        },
      ],
    }),
    headers: {
      "Content-type": "application/json",
      Authorization:
        `Bearer ${open_api_key}`, 
    },
  })
    .then((response) => response.json())
    .then((data) => {
      let output = data.choices[0].message.content;
      console.log(output);
      output = output.replace(/\n/g, "<br />");
      document.getElementById("result").innerHTML = output;
      document.getElementById("send").style.display = "inline";
      document.getElementById("loading").style.display = "none";
    })
    .catch((error) => {
      console.error("Error:", error);
      document.getElementById("result").innerHTML = "An error occurred. Please try again.";
      document.getElementById("send").style.display = "inline";
      document.getElementById("loading").style.display = "none";
    });;
});