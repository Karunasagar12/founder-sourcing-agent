import React, { useState } from 'react'
import { Code, User, Target, ChevronRight, ExternalLink, Database, Brain, Zap, Users, TrendingUp, Heart, Globe } from 'lucide-react'

const About = () => {
  const [activeTab, setActiveTab] = useState('project')

  const tabs = [
    { id: 'project', label: 'The Project', icon: Code },
    { id: 'about', label: 'About Me', icon: User },
    { id: 'pioneers', label: 'Why Pioneers?', icon: Target },
  ]

  const TabContent = () => {
    switch (activeTab) {
      case 'project':
        return (
          <div className="space-y-6">
            <div className="text-center mb-8">
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                Built in 30 Hours to Show What I Can Do
              </h1>
              <p className="text-lg text-gray-600 max-w-3xl mx-auto">
                A production-ready founder sourcing agent with complete cloud infrastructure, 
                live deployment, and automated CI/CD pipeline.
              </p>
            </div>

            {/* Live Application */}
            <div className="card bg-gradient-to-r from-green-50 to-emerald-50 border-green-200">
              <div className="flex items-center space-x-3 mb-4">
                <div className="p-2 bg-green-100 rounded-lg">
                  <Globe className="h-5 w-5 text-green-600" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900">🚀 Live Application</h3>
              </div>
              <div className="space-y-3">
                <p className="text-gray-700">
                  This application is <strong>live and accessible worldwide</strong> with a complete production infrastructure:
                </p>
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">Frontend (Firebase Hosting)</h4>
                    <p className="text-sm text-gray-600">
                      Deployed to <strong>https://founder-sourcing-agent.web.app</strong> with custom domain, 
                      HTTPS, and global CDN distribution.
                    </p>
                  </div>
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">Backend (Google Cloud Run)</h4>
                    <p className="text-sm text-gray-600">
                      Containerized FastAPI service with auto-scaling, load balancing, and 
                      production-grade monitoring.
                    </p>
                  </div>
                </div>
              </div>
            </div>

            <div className="grid md:grid-cols-2 gap-6">
              {/* Tech Stack */}
              <div className="card">
                <div className="flex items-center space-x-3 mb-4">
                  <div className="p-2 bg-blue-100 rounded-lg">
                    <Code className="h-5 w-5 text-blue-600" />
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900">Tech Stack</h3>
                </div>
                <div className="space-y-3">
                  <div className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-blue-600 rounded-full"></div>
                    <span className="text-gray-700">React + Vite (Frontend)</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-blue-600 rounded-full"></div>
                    <span className="text-gray-700">FastAPI (Backend)</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-blue-600 rounded-full"></div>
                    <span className="text-gray-700">Google Gemini AI (Analysis)</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-blue-600 rounded-full"></div>
                    <span className="text-gray-700">Harvest API (Data Source)</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-blue-600 rounded-full"></div>
                    <span className="text-gray-700">PostgreSQL + SQLAlchemy (Database)</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-blue-600 rounded-full"></div>
                    <span className="text-gray-700">Docker + Cloud Run (Deployment)</span>
                  </div>
                </div>
              </div>

              {/* Production Infrastructure */}
              <div className="card">
                <div className="flex items-center space-x-3 mb-4">
                  <div className="p-2 bg-purple-100 rounded-lg">
                    <TrendingUp className="h-5 w-5 text-purple-600" />
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900">Production Infrastructure</h3>
                </div>
                <div className="space-y-3">
                  <div className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-purple-600 rounded-full"></div>
                    <span className="text-gray-700">Google Cloud Platform (GCP)</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-purple-600 rounded-full"></div>
                    <span className="text-gray-700">Firebase Hosting (Frontend)</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-purple-600 rounded-full"></div>
                    <span className="text-gray-700">Cloud Run (Backend)</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-purple-600 rounded-full"></div>
                    <span className="text-gray-700">Cloud SQL PostgreSQL</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-purple-600 rounded-full"></div>
                    <span className="text-gray-700">GitHub Actions (CI/CD)</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Key Features */}
            <div className="card">
              <div className="flex items-center space-x-3 mb-4">
                <div className="p-2 bg-green-100 rounded-lg">
                  <Zap className="h-5 w-5 text-green-600" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900">Key Features</h3>
              </div>
              <div className="grid md:grid-cols-2 gap-4">
                <div className="space-y-3">
                  <div className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-green-600 rounded-full"></div>
                    <span className="text-gray-700">AI-powered candidate analysis</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-green-600 rounded-full"></div>
                    <span className="text-gray-700">Intelligent tier ranking (A/B/C)</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-green-600 rounded-full"></div>
                    <span className="text-gray-700">CSV export functionality</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-green-600 rounded-full"></div>
                    <span className="text-gray-700">User authentication system</span>
                  </div>
                </div>
                <div className="space-y-3">
                  <div className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-green-600 rounded-full"></div>
                    <span className="text-gray-700">Automated CI/CD pipeline</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-green-600 rounded-full"></div>
                    <span className="text-gray-700">Production monitoring & logging</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-green-600 rounded-full"></div>
                    <span className="text-gray-700">Database migrations</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-green-600 rounded-full"></div>
                    <span className="text-gray-700">Responsive, modern UI</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Technical Challenges */}
            <div className="card">
              <div className="flex items-center space-x-3 mb-4">
                <div className="p-2 bg-orange-100 rounded-lg">
                  <Brain className="h-5 w-5 text-orange-600" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900">Technical Challenges Solved</h3>
              </div>
              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <h4 className="font-medium text-gray-900 mb-2">AI Integration</h4>
                  <p className="text-gray-600 text-sm">
                    Seamlessly integrated Google Gemini AI for intelligent candidate analysis, 
                    handling rate limits and API responses efficiently.
                  </p>
                </div>
                <div>
                  <h4 className="font-medium text-gray-900 mb-2">Data Processing</h4>
                  <p className="text-gray-600 text-sm">
                    Built robust data pipelines to process and analyze large datasets from 
                    Harvest API with proper error handling and validation.
                  </p>
                </div>
                <div>
                  <h4 className="font-medium text-gray-900 mb-2">Production Deployment</h4>
                  <p className="text-gray-600 text-sm">
                    Implemented complete cloud infrastructure with automated CI/CD, 
                    containerization, and production-grade security.
                  </p>
                </div>
                <div>
                  <h4 className="font-medium text-gray-900 mb-2">Scalable Architecture</h4>
                  <p className="text-gray-600 text-sm">
                    Designed microservices architecture with auto-scaling, load balancing, 
                    and database connection pooling for production workloads.
                  </p>
                </div>
                <div>
                  <h4 className="font-medium text-gray-900 mb-2">Security & Authentication</h4>
                  <p className="text-gray-600 text-sm">
                    Implemented JWT authentication, CORS configuration, environment-based 
                    security, and secure API key management.
                  </p>
                </div>
                <div>
                  <h4 className="font-medium text-gray-900 mb-2">DevOps Automation</h4>
                  <p className="text-gray-600 text-sm">
                    Created automated deployment pipeline with testing, building, and 
                    deployment to multiple cloud services with zero-downtime updates.
                  </p>
                </div>
              </div>
            </div>

            {/* Production Achievements */}
            <div className="card bg-gradient-to-r from-blue-50 to-indigo-50 border-blue-200">
              <div className="flex items-center space-x-3 mb-4">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <Target className="h-5 w-5 text-blue-600" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900">Production Achievements</h3>
              </div>
              <div className="space-y-4">
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">🚀 Live Deployment</h4>
                    <ul className="space-y-1 text-sm text-gray-600">
                      <li>• Custom domain with HTTPS</li>
                      <li>• Global CDN distribution</li>
                      <li>• Auto-scaling infrastructure</li>
                      <li>• Production monitoring</li>
                    </ul>
                  </div>
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">🔧 DevOps Excellence</h4>
                    <ul className="space-y-1 text-sm text-gray-600">
                      <li>• Automated CI/CD pipeline</li>
                      <li>• Containerized microservices</li>
                      <li>• Database migrations</li>
                      <li>• Environment management</li>
                    </ul>
                  </div>
                </div>
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">🛡️ Security & Reliability</h4>
                    <ul className="space-y-1 text-sm text-gray-600">
                      <li>• JWT authentication</li>
                      <li>• CORS configuration</li>
                      <li>• Secure API management</li>
                      <li>• Database backups</li>
                    </ul>
                  </div>
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">📊 Performance & Scale</h4>
                    <ul className="space-y-1 text-sm text-gray-600">
                      <li>• Load balancing</li>
                      <li>• Connection pooling</li>
                      <li>• Caching strategies</li>
                      <li>• Cost optimization</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>

            {/* What's Next */}
            <div className="card bg-gradient-to-r from-green-50 to-emerald-50 border-green-200">
              <div className="flex items-center space-x-3 mb-4">
                <div className="p-2 bg-green-100 rounded-lg">
                  <TrendingUp className="h-5 w-5 text-green-600" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900">What Could Be Built Next</h3>
              </div>
              <div className="space-y-3">
                <p className="text-gray-700">
                  With this solid production foundation, the platform could evolve into:
                </p>
                <ul className="space-y-2 text-gray-600">
                  <li className="flex items-center space-x-2">
                    <ChevronRight className="h-4 w-4 text-green-600" />
                    <span>Advanced ML models for predictive candidate scoring</span>
                  </li>
                  <li className="flex items-center space-x-2">
                    <ChevronRight className="h-4 w-4 text-green-600" />
                    <span>Multi-source data integration (LinkedIn, Crunchbase, etc.)</span>
                  </li>
                  <li className="flex items-center space-x-2">
                    <ChevronRight className="h-4 w-4 text-green-600" />
                    <span>Real-time collaboration features for team evaluation</span>
                  </li>
                  <li className="flex items-center space-x-2">
                    <ChevronRight className="h-4 w-4 text-green-600" />
                    <span>Advanced analytics dashboard with insights</span>
                  </li>
                  <li className="flex items-center space-x-2">
                    <ChevronRight className="h-4 w-4 text-green-600" />
                    <span>API marketplace for third-party integrations</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        )

      case 'about':
        return (
          <div className="space-y-6">
            <div className="text-center mb-8">
              <div className="mb-6">
                <img 
                  src="/3C0A4376.JPG" 
                  alt="Karunasagar Mohansundar" 
                  className="w-32 h-32 rounded-full mx-auto mb-4 object-cover border-4 border-blue-100 shadow-lg"
                />
              </div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                Healthcare Data Scientist Turned Entrepreneurial Builder
              </h1>
              <p className="text-lg text-gray-600 max-w-3xl mx-auto">
                Bridging the gap between complex healthcare data and actionable business solutions
              </p>
            </div>

            {/* My Journey */}
            <div className="card">
              <div className="flex items-center space-x-3 mb-4">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <User className="h-5 w-5 text-blue-600" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900">My Journey</h3>
              </div>
              <div className="space-y-4 text-gray-700">
                <p>
                  Started with an integrated MSc in Data Science in India, where I built a strong technical 
                  foundation in AI, machine learning, and analytics. Transitioned into healthcare data roles 
                  at <strong>EXL</strong>, <strong>MiiCare</strong>, and <strong>Zelis</strong> — designing predictive models, 
                  real-time monitoring systems, and large-scale analytics frameworks that saved costs and 
                  improved patient outcomes.
                </p>
                <p>
                  Today, as an MSc student in <strong>Healthcare Management & Data Intelligence</strong> 
                  (emlyon/Mines), I'm adding the strategic, entrepreneurial layer to turn those skills into ventures.
                </p>
              </div>
            </div>

            {/* What Drives Me */}
            <div className="card bg-gradient-to-r from-green-50 to-emerald-50 border-green-200">
              <div className="flex items-center space-x-3 mb-4">
                <div className="p-2 bg-green-100 rounded-lg">
                  <Heart className="h-5 w-5 text-green-600" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900">What Drives Me</h3>
              </div>
              <div className="space-y-4 text-gray-700">
                <p>
                  Healthcare is the biggest stage where technology can save lives and cut costs — and yet 
                  adoption lags behind. I'm driven by the challenge of translating complex science and data 
                  into solutions that hospitals, payers, and patients actually use.
                </p>
                <p>
                  <strong>Curiosity</strong> fuels my learning; <strong>ambition</strong> fuels my building.
                </p>
              </div>
            </div>

            {/* Skills Showcase */}
            <div className="grid md:grid-cols-3 gap-6">
              <div className="card">
                <div className="flex items-center space-x-3 mb-4">
                  <div className="p-2 bg-purple-100 rounded-lg">
                    <Code className="h-5 w-5 text-purple-600" />
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900">Technical</h3>
                </div>
                <div className="space-y-2 text-sm text-gray-600">
                  <div className="flex items-center space-x-2">
                    <div className="w-1.5 h-1.5 bg-purple-600 rounded-full"></div>
                    <span>AI/ML (Python, PyTorch)</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-1.5 h-1.5 bg-purple-600 rounded-full"></div>
                    <span>SQL, PySpark</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-1.5 h-1.5 bg-purple-600 rounded-full"></div>
                    <span>Predictive Analytics</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-1.5 h-1.5 bg-purple-600 rounded-full"></div>
                    <span>Digital Health Tools</span>
                  </div>
                </div>
              </div>

              <div className="card">
                <div className="flex items-center space-x-3 mb-4">
                  <div className="p-2 bg-blue-100 rounded-lg">
                    <Target className="h-5 w-5 text-blue-600" />
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900">Product & Strategy</h3>
                </div>
                <div className="space-y-2 text-sm text-gray-600">
                  <div className="flex items-center space-x-2">
                    <div className="w-1.5 h-1.5 bg-blue-600 rounded-full"></div>
                    <span>Go-to-market Design</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-1.5 h-1.5 bg-blue-600 rounded-full"></div>
                    <span>Venture Concepting</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-1.5 h-1.5 bg-blue-600 rounded-full"></div>
                    <span>Stakeholder Engagement</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-1.5 h-1.5 bg-blue-600 rounded-full"></div>
                    <span>Healthcare Economics</span>
                  </div>
                </div>
              </div>

              <div className="card">
                <div className="flex items-center space-x-3 mb-4">
                  <div className="p-2 bg-green-100 rounded-lg">
                    <Users className="h-5 w-5 text-green-600" />
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900">Leadership</h3>
                </div>
                <div className="space-y-2 text-sm text-gray-600">
                  <div className="flex items-center space-x-2">
                    <div className="w-1.5 h-1.5 bg-green-600 rounded-full"></div>
                    <span>Team-building</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-1.5 h-1.5 bg-green-600 rounded-full"></div>
                    <span>Cross-cultural Collaboration</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-1.5 h-1.5 bg-green-600 rounded-full"></div>
                    <span>Founder Mindset</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-1.5 h-1.5 bg-green-600 rounded-full"></div>
                    <span>Market Entry Strategy</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Why I Love Building */}
            <div className="card bg-gradient-to-r from-orange-50 to-amber-50 border-orange-200">
              <div className="flex items-center space-x-3 mb-4">
                <div className="p-2 bg-orange-100 rounded-lg">
                  <Zap className="h-5 w-5 text-orange-600" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900">Why I Love Building Things</h3>
              </div>
              <div className="text-gray-700">
                <p>
                  Because every build — whether a model, a pipeline, or a startup idea — is a way to move 
                  from abstract potential to tangible impact. What excites me most is that feeling when 
                  something I've created makes others' work easier, patients' care better, or a team more energized.
                </p>
              </div>
            </div>
          </div>
        )

      case 'pioneers':
        return (
          <div className="space-y-6">
            <div className="text-center mb-8">
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                Ready to Help Build Europe's Next Unicorns
              </h1>
              <p className="text-lg text-gray-600 max-w-3xl mx-auto">
                Bringing healthcare data expertise and rapid prototyping skills to Pioneers' mission
              </p>
            </div>

            {/* What I Know About Pioneers */}
            <div className="card">
              <div className="flex items-center space-x-3 mb-4">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <Globe className="h-5 w-5 text-blue-600" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900">What I Know About Pioneers</h3>
              </div>
              <div className="space-y-4 text-gray-700">
                <p>
                  Pioneers is unique because it doesn't just invest — it builds. The AI Lab at Station F 
                  reflects that DNA: shipping micro-products in 30 days, embedding founder empathy, and 
                  creating the same high-pressure environment startups face.
                </p>
                <p>
                  The ethos of <strong>"Take your shot. Build something exceptional."</strong> resonates 
                  deeply with me. It's exactly the kind of environment where I thrive — rapid iteration, 
                  bold experimentation, and real-world impact.
                </p>
              </div>
            </div>

            {/* Companies I Admire */}
            <div className="card bg-gradient-to-r from-purple-50 to-indigo-50 border-purple-200">
              <div className="flex items-center space-x-3 mb-4">
                <div className="p-2 bg-purple-100 rounded-lg">
                  <TrendingUp className="h-5 w-5 text-purple-600" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900">Companies/Investments I Admire</h3>
              </div>
              <div className="space-y-4 text-gray-700">
                <p>
                  I admire how Pioneers has backed and shaped ventures like <strong>Jina AI</strong> and 
                  <strong>Spoke.ai</strong>, which show that bold, experimental product building in Europe 
                  can compete globally.
                </p>
                <p>
                  I also appreciate Pioneers' early bet on automation and agentic AI tools, which aligns 
                  with where I see the most transformative potential — especially in healthcare, where 
                  AI can dramatically improve outcomes and reduce costs.
                </p>
              </div>
            </div>

            {/* What I'd Contribute */}
            <div className="grid md:grid-cols-2 gap-6">
              <div className="card">
                <div className="flex items-center space-x-3 mb-4">
                  <div className="p-2 bg-green-100 rounded-lg">
                    <Code className="h-5 w-5 text-green-600" />
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900">Technical Contributions</h3>
                </div>
                <div className="space-y-3 text-gray-700">
                  <p className="text-sm">
                    I bring the ability to prototype AI products quickly, with a healthcare and data 
                    science edge. My experience building predictive models and real-time systems translates 
                    directly to rapid product development.
                  </p>
                  <ul className="space-y-1 text-sm text-gray-600">
                    <li className="flex items-center space-x-2">
                      <ChevronRight className="h-3 w-3 text-green-600" />
                      <span>Rapid AI product prototyping</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <ChevronRight className="h-3 w-3 text-green-600" />
                      <span>Healthcare data expertise</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <ChevronRight className="h-3 w-3 text-green-600" />
                      <span>Scalable system architecture</span>
                    </li>
                  </ul>
                </div>
              </div>

              <div className="card">
                <div className="flex items-center space-x-3 mb-4">
                  <div className="p-2 bg-blue-100 rounded-lg">
                    <Users className="h-5 w-5 text-blue-600" />
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900">Cultural Contributions</h3>
                </div>
                <div className="space-y-3 text-gray-700">
                  <p className="text-sm">
                    Beyond code, I bring energy, resilience, and culture-building — from leading 
                    predictive analytics initiatives in healthcare to founding wellness programs 
                    that boosted team engagement.
                  </p>
                  <ul className="space-y-1 text-sm text-gray-600">
                    <li className="flex items-center space-x-2">
                      <ChevronRight className="h-3 w-3 text-blue-600" />
                      <span>Team leadership & motivation</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <ChevronRight className="h-3 w-3 text-blue-600" />
                      <span>Cross-cultural collaboration</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <ChevronRight className="h-3 w-3 text-blue-600" />
                      <span>Regulated sector experience</span>
                    </li>
                  </ul>
                </div>
              </div>
            </div>

            {/* My Future Vision */}
            <div className="card bg-gradient-to-r from-blue-50 to-indigo-50 border-blue-200">
              <div className="flex items-center space-x-3 mb-4">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <Target className="h-5 w-5 text-blue-600" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900">My Future Vision</h3>
              </div>
              <div className="space-y-4 text-gray-700">
                <div>
                  <h4 className="font-medium text-gray-900 mb-2">Short Term</h4>
                  <p className="text-sm">
                    Help Pioneers ship AI tools that supercharge founders and internal workflows. 
                    Focus on rapid prototyping and validation of new product concepts.
                  </p>
                </div>
                <div>
                  <h4 className="font-medium text-gray-900 mb-2">Long Term</h4>
                  <p className="text-sm">
                    Scale into a co-founder role within the Pioneers ecosystem, particularly at the 
                    intersection of healthtech and frontier computing. Build ventures that not only 
                    achieve scale but also create lasting value for society.
                  </p>
                </div>
              </div>
            </div>

            {/* Closing */}
            <div className="text-center">
              <div className="inline-block bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-8 py-4 rounded-lg shadow-lg">
                <h3 className="text-xl font-bold mb-2">Let's make something amazing together.</h3>
                <p className="text-blue-100">Ready to build Europe's next unicorns</p>
              </div>
            </div>
          </div>
        )

      default:
        return null
    }
  }

  return (
    <div className="max-w-6xl mx-auto">
      {/* Tab Navigation */}
      <div className="mb-8">
        <div className="flex flex-wrap gap-2 bg-white rounded-lg p-2 shadow-sm border border-gray-200">
          {tabs.map((tab) => {
            const Icon = tab.icon
            const isActive = activeTab === tab.id
            
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 px-4 py-3 rounded-lg text-sm font-medium transition-all duration-200 ${
                  isActive
                    ? 'bg-blue-100 text-blue-700 shadow-sm'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                }`}
              >
                <Icon className="h-4 w-4" />
                <span>{tab.label}</span>
              </button>
            )
          })}
        </div>
      </div>

      {/* Tab Content */}
      <div className="animate-fadeIn">
        <TabContent />
      </div>
    </div>
  )
}

export default About
