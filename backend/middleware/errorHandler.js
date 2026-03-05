function errorHandler(err, req, res, next) {
    console.error("❌ Internal server error:", err);
  
    res.status(500).json({
      error: "Internal server error",
      details: process.env.NODE_ENV === "development" ? err.message : undefined
    });
  }
  
  module.exports = errorHandler;
  