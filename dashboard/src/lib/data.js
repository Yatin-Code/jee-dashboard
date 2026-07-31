let data = null;
let loading = false;
let listeners = [];

export function getData() {
  return data;
}

export function subscribe(fn) {
  listeners.push(fn);
  return () => {
    listeners = listeners.filter((l) => l !== fn);
  };
}

export function loadData() {
  if (data) return Promise.resolve(data);
  if (loading) return new Promise((r) => subscribe(() => r(data)));
  loading = true;
  return fetch("data.json")
    .then((r) => r.json())
    .then((d) => {
      data = d;
      loading = false;
      listeners.forEach((fn) => fn());
      listeners = [];
      return data;
    })
    .catch((err) => {
      console.error("Failed to load data:", err);
      loading = false;
      return null;
    });
}
