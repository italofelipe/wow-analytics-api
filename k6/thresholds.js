/**
 * SLOs shared across all k6 scenarios.
 * Fail the test if any threshold is violated.
 */
export const thresholds = {
  // Error rate < 1% for all requests
  http_req_failed: [{ threshold: "rate<0.01", abortOnFail: true }],

  // Global p95 < 1s (each scenario can tighten this per group)
  http_req_duration: ["p(95)<1000"],

  // Per-endpoint SLOs (tagged via group() in scenarios)
  "http_req_duration{endpoint:health}":       ["p(95)<50"],
  "http_req_duration{endpoint:character}":    ["p(95)<500"],
  "http_req_duration{endpoint:snapshots}":    ["p(95)<300"],
  "http_req_duration{endpoint:runs}":         ["p(95)<400"],
  "http_req_duration{endpoint:stats_classes}":["p(95)<200"],
};
