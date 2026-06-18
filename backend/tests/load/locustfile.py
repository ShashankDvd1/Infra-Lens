from locust import HttpUser, task, between
import random

class LandScopeUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def view_map_markers(self):
        """Simulate loading map markers (should be heavily cached)."""
        cities = ["Lucknow", "Pune", "Hyderabad"]
        city = random.choice(cities)
        self.client.get(f"/api/v1/map/markers?city={city}", name="/api/v1/map/markers")

    @task(2)
    def view_projects_list(self):
        """Simulate browsing the projects directory."""
        self.client.get("/api/v1/projects/?skip=0&limit=20", name="/api/v1/projects/")

    @task(1)
    def search_projects(self):
        """Simulate semantic search."""
        queries = ["commercial plot near metro", "upcoming airport expressway", "IT park development"]
        query = random.choice(queries)
        self.client.get(f"/api/v1/search/semantic?query={query}&limit=5", name="/api/v1/search/semantic")

    @task(1)
    def view_health(self):
        """Check system health."""
        self.client.get("/health", name="/health")
