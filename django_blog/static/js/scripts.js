document.addEventListener("DOMContentLoaded", () => {
  console.log("Django Blog loaded successfully!");

  // Example interaction: Alert when clicking "Read More" (Temporary)
  const readLinks = document.querySelectorAll(".read-more");

  readLinks.forEach((link) => {
    link.addEventListener("click", (e) => {
      // Prevent default just for this demo
      // Remove this block when you implement real links
      console.log("Read more clicked");
    });
  });
});