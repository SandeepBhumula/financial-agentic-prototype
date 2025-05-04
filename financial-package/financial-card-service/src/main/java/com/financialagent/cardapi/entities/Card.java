package com.financialagent.cardapi.entities;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.LocalDate;
import java.time.OffsetDateTime;

@Entity
@Table(name = "Card", schema = "cards",
       indexes = {
           @Index(name = "IX_Card_Status", columnList = "status"),
           @Index(name = "UQ_Card_LastFour_CustomerId", columnList = "last_four_digits, customer_id", unique = true),
           @Index(name = "UQ_Card_NumberHash", columnList = "card_number_hash", unique = true)
       })
@Data // Lombok: Generates getters, setters, toString, equals, hashCode
@NoArgsConstructor
public class Card {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "card_number_hash", nullable = false, unique = true)
    private String cardNumberHash; // Store a secure hash, not the real PAN

    @Column(name = "last_four_digits", nullable = false, length = 4)
    private String lastFourDigits;

    @Column(name = "cardholder_name")
    private String cardholderName;

    @Column(name = "expiry_date", nullable = false)
    @Temporal(TemporalType.DATE)
    private LocalDate expiryDate;

    @Column(nullable = false, length = 20)
    @Enumerated(EnumType.STRING)
    private CardStatus status;

    @Column(name = "customer_id", nullable = false, length = 100)
    private String customerId;

    @Column(name = "activation_date")
    private OffsetDateTime activationDate;

    @Column(name = "deactivation_date")
    private OffsetDateTime deactivationDate;

    @Column(name = "deactivation_reason")
    private String deactivationReason;

    @Column(name = "created_at", nullable = false, updatable = false)
    @CreationTimestamp // Automatically set by Hibernate on creation
    private OffsetDateTime createdAt;

    @Column(name = "updated_at", nullable = false)
    @UpdateTimestamp // Automatically set by Hibernate on creation and update
    private OffsetDateTime updatedAt;

    // Enum for card status - provides type safety
    public enum CardStatus {
        PRE_ACTIVATED, // Card issued but not yet active
        ACTIVE,
        DEACTIVATED,
        EXPIRED,
        LOST,
        STOLEN
    }
} 