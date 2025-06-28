const chatBox = document.getElementById('chat-box');

async function askAI() {
  const input = document.getElementById('user-input');
  const userText = input.value.trim();
  if (!userText) return;

  chatBox.innerHTML += `<p><strong>You:</strong> ${userText}</p>`;
  input.value = '';

  const response = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer YOUR_OPENAI_API_KEY'
    },
    body: JSON.stringify({
      model: 'gpt-4',
      messages: [{ role: 'user', content: userText }]
    })
  });

  const data = await response.json();
  const aiReply = data.choices[0].message.content;
  chatBox.innerHTML += `<p><strong>AI:</strong> ${aiReply}</p>`;
  chatBox.scrollTop = chatBox.scrollHeight;
}

const projects = [
  {
    name: 'Excel Stock Automation',
    description: 'Automates ceramic tile stock management using Excel VBA and triggers smart alerts for dispatch mismatches.'
  },
  {
    name: 'Secure Web Inventory App',
    description: 'Web-based inventory tool with password-protected actions, CSV import/export, and real-time stock alerts.'
  },
  {
    name: 'AI-Powered Resume Analyzer',
    description: 'GPT-based tool that evaluates resumes and offers suggestions based on job role alignment.'
  }
];

const list = document.getElementById('project-list');
projects.forEach(p => {
  const item = document.createElement('div');
  item.innerHTML = `<h3>${p.name}</h3><p>${p.description}</p>`;
  list.appendChild(item);
});

// Typed.js animated tagline
new Typed('#typed', {
  strings: ['AI & Automation Developer', 'Web & Excel Solutions Expert', 'Creative Technologist'],
  typeSpeed: 50,
  backSpeed: 30,
  loop: true
});
