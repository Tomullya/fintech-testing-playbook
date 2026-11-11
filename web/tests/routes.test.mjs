// Routing of the playbook site.
import { test } from "node:test";
import assert from "node:assert/strict";
import { href, parse } from "../js/routes.js";

const known = ["home", "01-card-payment", "03-money", "glossary"];

test("home for empty and root hashes", () => {
  assert.deepEqual(parse("", known), { page: "home", anchor: "" });
  assert.deepEqual(parse("#/", known), { page: "home", anchor: "" });
});

test("page and Cyrillic anchor, encoded or not", () => {
  assert.deepEqual(parse("#/03-money/округление", known), { page: "03-money", anchor: "округление" });
  assert.deepEqual(parse(href("03-money", "округление"), known), { page: "03-money", anchor: "округление" });
});

test("unknown page falls back to home", () => {
  assert.deepEqual(parse("#/99-nope/x", known), { page: "home", anchor: "" });
});

test("broken percent-encoding does not throw", () => {
  assert.deepEqual(parse("#/03-money/%E0%A4%A", known), { page: "03-money", anchor: "%E0%A4%A" });
});

test("href", () => {
  assert.equal(href("home"), "#/");
  assert.equal(href("glossary"), "#/glossary");
});
