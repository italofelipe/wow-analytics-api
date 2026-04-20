/**
 * Smoke test — 1 VU, 1 min.
 * Validates the API is up and not broken. Runs on every merge to main.
 */
import http from "k6/http";
import { check, group, sleep } from "k6";
import { thresholds } from "../thresholds.js";

const BASE_URL = __ENV.BASE_URL || "http://localhost:8000";

export const options = {
  vus: 1,
  duration: "1m",
  thresholds,
};

export default function () {
  group("health", function () {
    const res = http.get(`${BASE_URL}/health`, {
      tags: { endpoint: "health" },
    });
    check(res, {
      "health status 200": (r) => r.status === 200,
    });
  });

  group("stats_classes", function () {
    const res = http.get(`${BASE_URL}/stats/classes?region=us`, {
      tags: { endpoint: "stats_classes" },
    });
    check(res, {
      "stats/classes 200 or 503": (r) => [200, 503].includes(r.status),
    });
  });

  sleep(1);
}
