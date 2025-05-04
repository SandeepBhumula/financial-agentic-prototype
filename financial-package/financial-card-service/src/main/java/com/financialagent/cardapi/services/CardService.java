package com.financialagent.cardapi.services;

import com.financialagent.cardapi.entities.Card;
import com.financialagent.cardapi.exceptions.CardNotFoundException;
import com.financialagent.cardapi.exceptions.InvalidCardStateException;
import com.financialagent.cardapi.exceptions.ValidationException;

import java.util.List;

public interface CardService {

    /**
     * Get all cards belonging to a customer
     * 
     * @param customerId The ID of the customer
     * @return List of cards belonging to the customer
     */
    List<Card> getCardsByCustomerId(String customerId);
    
    /**
     * Get a specific card by ID, validating customer ownership
     * 
     * @param cardId The ID of the card to retrieve
     * @param customerId The ID of the customer who should own the card
     * @return The card if found and owned by the customer
     * @throws CardNotFoundException if the card doesn't exist or doesn't belong to the customer
     */
    Card getCardById(String cardId, String customerId) throws CardNotFoundException;

    /**
     * Activates a card based on its last four digits, CVV, and expiry date.
     *
     * @param cardLastFour The last four digits of the card number.
     * @param cvv The Card Verification Value.
     * @param expiryDate The expiry date string (e.g., "MM/YY" or "YYYY-MM").
     * @param customerId The ID of the customer attempting the activation.
     * @return true if activation was successful.
     * @throws CardNotFoundException if the card cannot be found.
     * @throws InvalidCardStateException if the card is not in a state eligible for activation (e.g., already active, expired).
     * @throws ValidationException if CVV or expiry date validation fails.
     */
    boolean activateCard(String cardLastFour, String cvv, String expiryDate, String customerId)
            throws CardNotFoundException, InvalidCardStateException, ValidationException;

    /**
     * Deactivates a card based on its last four digits.
     *
     * @param cardLastFour The last four digits of the card number.
     * @param reason The reason for deactivation.
     * @param customerId The ID of the customer attempting the deactivation.
     * @return true if deactivation was successful.
     * @throws CardNotFoundException if the card cannot be found.
     * @throws InvalidCardStateException if the card is already deactivated or in another non-actionable state.
     */
    boolean deactivateCard(String cardLastFour, String reason, String customerId)
            throws CardNotFoundException, InvalidCardStateException;

    // We might add other methods later, e.g.:
    // Card blockCard(String cardLastFour, String reason, String customerId);
} 