# Lab 3 - Student Club Event Ticketing & Budget Portal

## Project Details
- Project Title: Student Club Event Ticketing & Budget Portal
- Primary Domain: Campus & Academic Operations
- Target Actors: Club Lead, Campus Admin
- Selected Architecture: Layered Architecture

## Final Submission Files
- `Component_Diagram(1)(1).drawio` - editable UML component diagram source.
- `UMLComponentDiagram.pdf` - exported component diagram PDF.
- `Architecture_Justification.pdf` - PDF version of the same justification.

## Component Diagram Coverage
The diagram contains 9 components across three layers:

### Presentation Layer
- Web Portal UI
- Venue Check-In UI

### Business / Application Layer
- Authentication & RBAC
- Event & Budget Workflow
- Ticketing & QR Generation
- QR Check-In Validation

### Data & Infrastructure Layer
- Notification Service
- Repository / Data Access
- Portal Database

The diagram shows labelled provided/required assembly interfaces, `<<use>>` dependencies, and database data flow. It uses black, white, and line styling only; no decorative colours are applied.

## Architecture Justification Coverage
The one-page justification includes:
- Scenario review
- Comparison of Layered, Microservices, and Client-Server styles
- Selected architecture
- Two scenario-specific reasons
- Security advantage
- Performance benefit
- Component and interface summary
