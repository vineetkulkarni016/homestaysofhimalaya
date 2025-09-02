const { test, expect } = require('@playwright/test');

const routes = [
  { path: '/', title: 'Welcome to Homestays of Himalaya' },
  { path: '/homestays', title: 'Homestay Listings' },
  { path: '/bookings', title: 'Your Bookings' },
  { path: '/profile', title: 'User Profile' },
];

const viewports = {
  mobile: { width: 375, height: 667 },
  tablet: { width: 768, height: 1024 },
  desktop: { width: 1440, height: 900 },
};

for (const route of routes) {
  test.describe(`${route.path} responsiveness`, () => {
    for (const [name, size] of Object.entries(viewports)) {
      test(`renders on ${name}`, async ({ page }) => {
        await page.setViewportSize(size);
        await page.goto(`http://localhost:3000${route.path}`);
        await expect(page.locator('h1')).toHaveText(route.title);
      });
    }

    test('navigation adapts between mobile and desktop', async ({ page }) => {
      await page.setViewportSize(viewports.mobile);
      await page.goto(`http://localhost:3000${route.path}`);
      await expect(page.getByRole('button', { name: 'Open menu' })).toBeVisible();
      await expect(page.locator('nav').getByText('Home')).toBeHidden();

      await page.setViewportSize(viewports.desktop);
      await page.goto(`http://localhost:3000${route.path}`);
      await expect(page.getByRole('button', { name: 'Open menu' })).toBeHidden();
      await expect(page.locator('nav').getByText('Home')).toBeVisible();
    });
  });
}
