# FreightCalculator Project Todo

## Phase 3: Implementasi fitur kalkulator freight sesuai UI mockup

### ✅ Completed
- [x] Fix Django server startup errors
- [x] Fix AUTH_USER_MODEL configuration
- [x] Fix serializer indentation error
- [x] Fix login template link text

### 🔄 In Progress
- [x] Add initial data for Country and Category models
- [x] Create CRUD views for Country and Category
- [x] Create dashboard template
- [ ] Implement freight calculator APIs
- [ ] Integrate with Raja Ongkir API
- [ ] Create Vue.js frontend calculator
- [ ] Add URL routing for dashboard and CRUD operations

### 📋 Detailed Tasks

#### 1. Database Setup
- [x] Create migration for Country and Category models
- [x] Add initial data (5 countries, 10+ categories)
- [x] Run migrations

#### 2. CRUD Operations
- [ ] Create Country CRUD views (list, create, update, delete)
- [ ] Create Category CRUD views (list, create, update, delete)
- [ ] Create templates for CRUD operations
- [ ] Add proper navigation between pages

#### 3. API Development
- [ ] Create API endpoint: /api/countries?search={}
- [ ] Create API endpoint: /api/categories?country_id={}&search={}
- [ ] Create API endpoint: /api/destination?search={city}
- [ ] Create API endpoint: /api/calculate
- [ ] Integrate Raja Ongkir API for domestic shipping

#### 4. Frontend Calculator
- [ ] Create Vue.js/Nuxt.js calculator component
- [ ] Implement UI matching the provided mockup
- [ ] Connect frontend to backend APIs
- [ ] Add responsive design

#### 5. Dashboard
- [ ] Create main dashboard template
- [ ] Add navigation menu
- [ ] Display calculator and CRUD links
- [ ] Add user authentication checks

