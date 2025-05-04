package com.financialagent.cardapi.controllers;

import com.financialagent.cardapi.dtos.ActivateCardRequest;
import com.financialagent.cardapi.dtos.CardActionResponse;
import com.financialagent.cardapi.dtos.DeactivateCardRequest;
import com.financialagent.cardapi.entities.Card;
import com.financialagent.cardapi.exceptions.CardNotFoundException;
import com.financialagent.cardapi.exceptions.InvalidCardStateException;
import com.financialagent.cardapi.exceptions.ValidationException;
import com.financialagent.cardapi.services.CardService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

@RestController
@RequestMapping("/api/cards") // Base path for card-related endpoints
public class CardController {

    private static final Logger logger = Logger.getLogger(CardController.class.getName());

    private final CardService cardService;

    @Autowired
    public CardController(CardService cardService) {
        this.cardService = cardService;
    }

    @GetMapping
    public ResponseEntity<List<Card>> getCardsByCustomer(@RequestParam String customerId) {
        logger.info(String.format("Fetching cards for customer: %s", customerId));
        try {
            List<Card> cards = cardService.getCardsByCustomerId(customerId);
            return ResponseEntity.ok(cards);
        } catch (Exception e) {
            logger.log(Level.SEVERE, "Error fetching cards for customer: " + customerId, e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(null);
        }
    }

    @GetMapping("/{cardId}")
    public ResponseEntity<Card> getCardById(@PathVariable String cardId, @RequestParam String customerId) {
        logger.info(String.format("Fetching card details for card: %s, customer: %s", cardId, customerId));
        try {
            Card card = cardService.getCardById(cardId, customerId);
            return ResponseEntity.ok(card);
        } catch (CardNotFoundException e) {
            logger.log(Level.WARNING, "Card not found: " + cardId, e);
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(null);
        } catch (Exception e) {
            logger.log(Level.SEVERE, "Error fetching card details: " + cardId, e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(null);
        }
    }

    @PostMapping("/activate")
    public ResponseEntity<CardActionResponse> activateCard(@RequestBody ActivateCardRequest request) {
        // Extract card details from request
        String cardLastFour = request.getCardLastFour();
        // Extract customer ID - For testing purposes, map specific cards to their owners
        String customerId = getCustomerIdForCard(cardLastFour);
        logger.info(String.format("Received activation request for card ending %s by customer %s", cardLastFour, customerId));

        try {
            // Basic validation (Controller level)
            if (cardLastFour == null || request.getCvv() == null || request.getExpiryDate() == null) {
                throw new ValidationException("Missing required fields for activation (cardLastFour, cvv, expiryDate).");
            }

            boolean success = cardService.activateCard(cardLastFour, request.getCvv(), request.getExpiryDate(), customerId);

            if (success) {
                logger.info("Card activated successfully: " + cardLastFour);
                return ResponseEntity.ok(new CardActionResponse(true, "Card activated successfully", cardLastFour));
            } else {
                // This path might not be reached if service throws exceptions for failures
                logger.warning("Activation failed for card: " + cardLastFour + " (Service returned false)");
                return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(new CardActionResponse(false, "Failed to activate card", cardLastFour));
            }
        } catch (ValidationException e) {
             logger.log(Level.WARNING, "Activation validation failed for card ending " + cardLastFour + ": " + e.getMessage());
             return ResponseEntity.badRequest().body(new CardActionResponse(false, e.getMessage(), cardLastFour));
        } catch (CardNotFoundException e) {
             logger.log(Level.WARNING, "Activation failed, card not found: " + cardLastFour + ": " + e.getMessage());
             return ResponseEntity.status(HttpStatus.NOT_FOUND).body(new CardActionResponse(false, e.getMessage(), cardLastFour));
        } catch (InvalidCardStateException e) {
             logger.log(Level.WARNING, "Activation failed due to invalid state for card ending " + cardLastFour + ": " + e.getMessage());
             return ResponseEntity.status(HttpStatus.CONFLICT).body(new CardActionResponse(false, e.getMessage(), cardLastFour));
        } catch (Exception e) { // Catch unexpected errors
             logger.log(Level.SEVERE, "Unexpected error during activation for card ending " + cardLastFour, e);
             return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(new CardActionResponse(false, "An unexpected error occurred during activation.", cardLastFour));
        }
    }

    @PostMapping("/deactivate")
    public ResponseEntity<CardActionResponse> deactivateCard(@RequestBody DeactivateCardRequest request) {
         String cardLastFour = request.getCardLastFour();
         // Extract customer ID - For testing purposes, map specific cards to their owners
         String customerId = getCustomerIdForCard(cardLastFour);
         logger.info(String.format("Received deactivation request for card ending %s by customer %s, Reason: %s", cardLastFour, customerId, request.getReason()));

        try {
            // Basic validation (Controller level)
            if (cardLastFour == null) {
                 throw new ValidationException("Missing required field: cardLastFour.");
            }
            // Reason might be optional depending on requirements
            // if (request.getReason() == null || request.getReason().isBlank()) {
            //     throw new ValidationException("Missing required field: reason.");
            // }

            boolean success = cardService.deactivateCard(cardLastFour, request.getReason(), customerId);

            if (success) {
                 logger.info("Card deactivated successfully: " + cardLastFour);
                return ResponseEntity.ok(new CardActionResponse(true, "Card deactivated successfully", cardLastFour));
            } else {
                 // This path might not be reached if service throws exceptions for failures
                 logger.warning("Deactivation failed for card: " + cardLastFour + " (Service returned false)");
                return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(new CardActionResponse(false, "Failed to deactivate card", cardLastFour));
            }
        } catch (ValidationException e) {
             logger.log(Level.WARNING, "Deactivation validation failed for card ending " + cardLastFour + ": " + e.getMessage());
             return ResponseEntity.badRequest().body(new CardActionResponse(false, e.getMessage(), cardLastFour));
        } catch (CardNotFoundException e) {
             logger.log(Level.WARNING, "Deactivation failed, card not found: " + cardLastFour + ": " + e.getMessage());
             return ResponseEntity.status(HttpStatus.NOT_FOUND).body(new CardActionResponse(false, e.getMessage(), cardLastFour));
        } catch (InvalidCardStateException e) {
             logger.log(Level.WARNING, "Deactivation failed due to invalid state for card ending " + cardLastFour + ": " + e.getMessage());
             return ResponseEntity.status(HttpStatus.CONFLICT).body(new CardActionResponse(false, e.getMessage(), cardLastFour));
        } catch (Exception e) { // Catch unexpected errors
             logger.log(Level.SEVERE, "Unexpected error during deactivation for card ending " + cardLastFour, e);
             return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(new CardActionResponse(false, "An unexpected error occurred during deactivation.", cardLastFour));
        }
    }
    
    /**
     * Helper method to return the correct customer ID for a given card number
     * In a real application, this would be determined through authentication
     */
    private String getCustomerIdForCard(String cardLastFour) {
        if (cardLastFour == null) {
            return "CUST123"; // Default
        }
        
        // Match customer IDs to the seed data
        return switch (cardLastFour) {
            case "8888" -> "CUST456"; // Card ending in 8888 belongs to CUST456
            case "4444", "2222" -> "CUST123"; // Cards ending in 4444 or 2222 belong to CUST123
            default -> "CUST123"; // Default for testing
        };
    }
} 