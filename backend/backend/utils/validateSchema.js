const REQUIRED_FIELDS = [
    "alert_id",
    "attacker",
    "victim",
    "function_code",
    "timestamp",
    "severity",
    "packet_trace",
    "llm_reasoning",
    "mitigation_action",
    "rule_based_action",
    "llm_verification",
    "current_status"
  ];
  
  function validateAlert(alert) {
    const missing = REQUIRED_FIELDS.filter((field) => !(field in alert));
    return {
      ok: missing.length === 0,
      missing
    };
  }
  
  function validateAll(alerts) {
    if (!Array.isArray(alerts)) {
      console.warn("⚠️ alerts.json is not an array");
      return;
    }
  
    alerts.forEach((alert) => {
      const { ok, missing } = validateAlert(alert);
      if (!ok) {
        console.warn(
          `⚠️ Alert ${alert.alert_id || "<no-id>"} is missing fields: ${missing.join(
            ", "
          )}`
        );
      }
    });
  }
  
  module.exports = {
    REQUIRED_FIELDS,
    validateAlert,
    validateAll
  };
  