# Spätere Verbesserungen

- Datenbanktests für direkte `INSERT`-, `UPDATE`- und `DELETE`-Operationen auf `transaction_splits` ergänzen, jeweils für explizite und über die Ursprungstransaktion geerbte Vorgangszuordnungen.
- API-Regressionstest ergänzen, der nach `PUT /api/transactions/{id}/splits` den aktualisierten Vorgangsstatus im für die UI verwendeten Folge-Datenfluss prüft.
