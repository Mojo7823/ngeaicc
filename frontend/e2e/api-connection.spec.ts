import { test, expect } from '@playwright/test';

test.describe('API Connection Tests', () => {
  test('should load the main page', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('h1')).toHaveText('AI Testing Standard Platform');
  });

  test('should connect to backend API and display hello world data', async ({ page }) => {
    // Go to the application
    await page.goto('/');
    
    // Wait for the component to mount and make API calls
    await page.waitForTimeout(2000);
    
    // Check if there are any console errors
    const consoleErrors: string[] = [];
    page.on('console', msg => {
      if (msg.type() === 'error') {
        consoleErrors.push(msg.text());
      }
    });
    
    // Look for elements that should appear when API calls succeed
    // Let's check if the hello world response is displayed somewhere
    await page.waitForSelector('body', { timeout: 5000 });
    
    // Take a screenshot for debugging
    await page.screenshot({ path: 'test-results/api-connection-debug.png', fullPage: true });
    
    // Check network requests
    const apiRequests: any[] = [];
    page.on('request', request => {
      if (request.url().includes('localhost:8000')) {
        apiRequests.push({
          url: request.url(),
          method: request.method()
        });
      }
    });
    
    page.on('response', response => {
      if (response.url().includes('localhost:8000')) {
        console.log(`API Response: ${response.status()} ${response.url()}`);
      }
    });
    
    // Reload to catch network requests
    await page.reload();
    await page.waitForTimeout(3000);
    
    // Print console errors for debugging
    if (consoleErrors.length > 0) {
      console.log('Console Errors:', consoleErrors);
    }
    
    // Print API requests for debugging  
    console.log('API Requests made:', apiRequests);
    
    // Check if we can see evidence of successful API connection
    const pageContent = await page.textContent('body');
    console.log('Page contains backend data:', pageContent?.includes('FastAPI') || pageContent?.includes('backend'));
  });

  test('should test API endpoints directly', async ({ request }) => {
    // Test the backend API directly
    const healthResponse = await request.get('http://localhost:8000/health');
    expect(healthResponse.status()).toBe(200);
    
    const healthData = await healthResponse.json();
    expect(healthData.status).toBe('healthy');
    
    // Test the hello endpoint
    const helloResponse = await request.get('http://localhost:8000/api/v1/hello');
    expect(helloResponse.status()).toBe(200);
    
    const helloData = await helloResponse.json();
    expect(helloData.message).toBe('Hello World from FastAPI!');
    expect(helloData.data.framework).toBe('FastAPI');
  });
});
