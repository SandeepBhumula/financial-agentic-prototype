package com.financialagent.cardapi.repositories;

import com.financialagent.cardapi.entities.Card;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface CardRepository extends JpaRepository<Card, Long> {

    /**
     * Finds a card by its unique hashed card number.
     * This should be the primary way to look up a card for actions when the full PAN is available (after hashing).
     *
     * @param cardNumberHash The hashed card number.
     * @return An Optional containing the Card if found, otherwise empty.
     */
    Optional<Card> findByCardNumberHash(String cardNumberHash);

    /**
     * Finds a card by the last four digits and the customer ID.
     * Useful when only partial card information is available, often used for verification or display.
     *
     * @param lastFourDigits The last four digits of the card number.
     * @param customerId The ID of the customer associated with the card.
     * @return An Optional containing the Card if found, otherwise empty.
     */
    Optional<Card> findByLastFourDigitsAndCustomerId(String lastFourDigits, String customerId);

    /**
     * Finds all cards belonging to a specific customer.
     * 
     * @param customerId The ID of the customer.
     * @return A list of cards belonging to the customer.
     */
    List<Card> findByCustomerId(String customerId);
    
    /**
     * Finds a card by its ID.
     * This extends the standard findById method from JpaRepository to use a String instead of Long.
     * 
     * @param id The ID of the card as a String.
     * @return An Optional containing the Card if found, otherwise empty.
     */
    default Optional<Card> findById(String id) {
        try {
            Long cardId = Long.parseLong(id);
            return findById(cardId);
        } catch (NumberFormatException e) {
            return Optional.empty();
        }
    }

    // Add other custom query methods if needed, e.g.:
    // List<Card> findByCustomerIdAndStatus(String customerId, Card.CardStatus status);
    // List<Card> findByExpiryDateBefore(LocalDate date);
} 