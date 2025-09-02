module.exports = {
  testDir: './tests',
  webServer: {
    command: 'npm run dev',
    port: 3000,
    reuseExistingServer: !process.env.CI,
    cwd: __dirname,
  },
};
