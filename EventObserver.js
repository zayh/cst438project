/**
 * @author Lyndsay Hackett
 */

class EventObserver {
	
	constructor() {
		
		this.observers = [];
	}
	
	subscribe(f) {
		
		this.observers.push(f);
	}
	
	unsubscribe(f) {
		
		this.observers = this.observers.filter(subscriber=>subscriber!== f)
	}
	
	notify(data) {
		
		this.observers.forEach(observer=>observer(data));
	}
}

const userInput = document.querySelector(".userEntered");			// The input field
const statusText = document.querySelector(".inputStatus");			// The p tag we want to update
const updateStatusText = text => (statusText.textContent = text); 	// The content to be added to the p tag

// Create a new observer
const inputObserver = new EventObserver();

// Subscribe to the text field content
inputObserver.subscribe(updateStatusText);

// Listen for events on the text field and notify the observer so the text in the p tag can be updated
userInput.addEventListener("keyup", e => {
  inputObserver.notify(e.target.value);
  
  // Arbitrary value to check against to give the user some feedback on their input
  if ((statusText.textContent.length) < 10)
  {
    statusText.style.color = "green";
  }
  
  else
  {
    statusText.style.color = "red";
    statusText.textContent = "Too many characters!";
  }
});