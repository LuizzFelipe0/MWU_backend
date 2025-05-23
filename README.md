
<h1>Backend API - Money With You (MWU)</h1>

<p><strong>Money With You (MWU)</strong> is a personal finance management backend developed with <strong>FastAPI</strong>. The system allows users to track and categorize their expenses, offering an organized view of their financial behavior over time.</p>

<p>In this system, each user manages their own set of financial records. Users can create categories (e.g., Food, Transport, Salary), register one-time or recurring expenses, and visualize their cash flow. The system ensures that each user only accesses their own data, maintaining privacy and data integrity.</p>

<h2>Core Features</h2>
<ul>
  <li>Expense and category management</li>
  <li>Recurring expense tracking</li>
  <li>Expense classification (e.g., income vs. spending)</li>
  <li>Timestamp tracking: created, updated, and soft-deleted records</li>
</ul>

<h2>Key Technologies</h2>
<ul>
  <li>FastAPI (backend framework)</li>
  <li>SQLAlchemy (ORM)</li>
  <li>PostgreSQL (relational database)</li>
  <li>Pydantic (data validation &amp; serialization)</li>
  <li>bcrypt (password hashing)</li>
</ul>

<h2>Design Principles</h2>
<ul>
  <li>Repository-Service pattern for clean architecture</li>
  <li>Separation of concerns between data access, business logic, and API layers</li>
  <li>Modular and scalable folder structure</li>
  <li>Soft delete logic for data retention</li>
  <li>UUID-based primary keys</li>
</ul>

<h2>Requirements</h2>
<ul>
  <li>Python 3.10+</li>
  <li>MySQL</li>
  <li>pip (for dependency management)</li>
</ul> 

