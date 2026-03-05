const express = require("express");
const cors = require("cors");
const path = require("path");

const alertsRouter = require("./routes/alerts");
const errorHandler = require("./middleware/errorHandler");

const app = express();

// Middleware
app.use(express.json());

// Enable CORS (for localhost frontend)
app.use(
  cors({
    origin: "*", // you can restrict later to http://localhost:5173 or 3000
  })
);

// Simple health check
app.get("/", (req, res) => {
  res.json({ status: "ok", message: "Grid-LLM dashboard backend running" });
});

// Alerts API routes
app.use("/alerts", alertsRouter);

// Error handler (must be after routes)
app.use(errorHandler);

// Start server
const PORT = process.env.PORT || 5001;   
app.listen(PORT, () => {
  console.log(`✅ Backend server listening on http://localhost:${PORT}`);
});

