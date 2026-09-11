# 64: Show each Service Status colour as a swatch in the Statuses table

Parent: docs/.scratch/service-statuses/spec.md
Decisions: docs/decisions/service-statuses.md
Prior art: src/domains/serviceconfig/statuses/components/ServiceStatusesTable.tsx

## Acceptance criteria

1. The Statuses table under Service Configurations shows a colour swatch beside each Status name, filled with the Status's stored colour.
2. The swatch carries the colour's hex value as an accessible label.
3. Statuses without a colour show the Brand's neutral swatch.

Out of scope: editing the colour (ticket 65).
