/**
 * Load test — 10 VUs, 5 min.
 * Simulates normal traffic. Run via workflow_dispatch or scheduled.
 */
import http from "k6/http";
import { check, group, sleep } from "k6";
import { thresholds } from "../thresholds.js";

const BASE_URL = __ENV.BASE_URL || "http://localhost:8000";

export const options = {
  stages: [
    { duration: "30s", target: 10 },  // ramp up
    { duration: "4m",  target: 10 },  // hold
    { duration: "30s", target: 0  },  // ramp down
  ],
  thresholds,
};

export default function () {
  group("health", function () {
    const res = http.get(`${BASE_URL}/health`, { tags: { endpoint: "health" } });
    check(res, { "200": (r) => r.status === 200 });
  });

  group("stats_classes", function () {
    const res = http.get(`${BASE_URL}/stats/classes?region=us`, {
      tags: { endpoint: "stats_classes" },
    });
    check(res, { "200 or 503": (r) => [200, 503].includes(r.status) });
  });

  sleep(Math.random() * 2 + 1);
}
