// IMPORTANT! PLEASE READ BEFORE USING THIS:
//
// 1. This is JavaScript. JavaScript is executed in a browser.
// You can execute javascript when you control a browser with some browser automation tools.
// To execute javascript from your code use the corresponding method provided by your tool, for example:
// JavascriptExecutor interface in Selenium Java
// ExecuteJavaScript method of WebDriver in Selenium for .Net
// page.evaluate method in puppeteer
// Please refer to docs of your favourite browser automation tool for more info
//
// 2. If you don't understand what UNDEFINED means in the javascript console, please read:
// When you execute the code in the javascript console of your browser, the console evaluates EACH expression
// and prints the returned value. And if your expression does not return any value (that is absolutely normal)
// then you see 'undefined' in the console. This is NOT AND ERROR!
//
// For better understanding type the following in the console:
// let myVar = 'foo' // defines myVar variable and sets it's value to 'foo'
// You will see undefined in the console as this exression does not return anything.
//
// Then type the following
// (() => 'bar')() // defines and calls a function that returns 'bar'
// You will see "bar" as the function returns this value
//
// And one more case. Type:
// ((a) => { b = a * 2 })(2) // defines and calls a function that does not return any value
// What you will see? Yep, you will see undefined
//
// Hope now you understand some javascript console basics :)
//
// 3. The callback can be not the final step in your process. That is fine when after the callback you also need to perform
// another action like button click, form submission, etc
// 
// 4. NO, we can't make the same script for hCaptcha as the callback is not defined inside globaly accessible variables.


// USAGE
// paste the function definition into the console and then call the function:
//
// let res = findRecaptchaClients()
// console.log(res)
//
// the function returns an array of objects with recaptcha parameters for each implementation found on the page



function findRecaptchaClients() {
    // eslint-disable-next-line camelcase
    if (typeof (___grecaptcha_cfg) !== 'undefined') {
      // eslint-disable-next-line camelcase, no-undef
      return Object.entries(___grecaptcha_cfg.clients).map(([cid, client]) => {
        const data = { id: cid, version: cid >= 10000 ? 'V3' : 'V2' };
        const objects = Object.entries(client).filter(([_, value]) => value && typeof value === 'object');
  
        objects.forEach(([toplevelKey, toplevel]) => {
          const found = Object.entries(toplevel).find(([_, value]) => (
            value && typeof value === 'object' && 'sitekey' in value && 'size' in value
          ));
       
          if (typeof toplevel === 'object' && toplevel instanceof HTMLElement && toplevel['tagName'] === 'DIV'){
              data.pageurl = toplevel.baseURI;
          }
          
          if (found) {
            const [sublevelKey, sublevel] = found;
  
            data.sitekey = sublevel.sitekey;
            const callbackKey = data.version === 'V2' ? 'callback' : 'promise-callback';
            const callback = sublevel[callbackKey];
            if (!callback) {
              data.callback = null;
              data.function = null;
            } else {
              data.function = callback;
              const keys = [cid, toplevelKey, sublevelKey, callbackKey].map((key) => `['${key}']`).join('');
              data.callback = `___grecaptcha_cfg.clients${keys}`;
            }
          }
        });
        return data;
      });
    }
    return [];
  }