/**
 * Stress test — ramp up to 50 VUs to find the breaking point.
 * Run via workflow_dispatch only. Never in automated CI.
 */
import http from "k6/http";
import { check, group, sleep } from "k6";

const BASE_URL = __ENV.BASE_URL || "http://localhost:8000";

export const options = {
  stages: [
    { duration: "1m",  target: 10 },
    { duration: "2m",  target: 25 },
    { duration: "2m",  target: 50 },
    { duration: "1m",  target: 0  },
  ],
  thresholds: {
    http_req_failed: ["rate<0.05"],  // allow up to 5% errors under stress
  },
};

export default function () {
  group("health", function () {
    const res = http.get(`${BASE_URL}/health`, { tags: { endpoint: "health" } });
    check(res, { "not 5xx": (r) => r.status < 500 });
  });

  group("stats_classes", function () {
    const res = http.get(`${BASE_URL}/stats/classes?region=us`, {
      tags: { endpoint: "stats_classes" },
    });
    check(res, { "not 5xx": (r) => r.status < 500 });
  });

  sleep(0.5);
}
