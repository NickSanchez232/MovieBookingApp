document.addEventListener('DOMContentLoaded', function() {
    initializeTheaterSelection();
    initializeSeatSelection();
    initializePaymentSelection();
    initializeStarRating();
    updateBookingSummary();
});

// Theater Selection
function initializeTheaterSelection() {
    const theaterOptions = document.querySelectorAll('.theater-option');
    
    theaterOptions.forEach(option => {
        option.addEventListener('click', function() {
            // Remove selected class from all options
            theaterOptions.forEach(opt => opt.classList.remove('selected'));
            
            // Add selected class to clicked option
            this.classList.add('selected');
            
            // Update hidden input if exists
            const theaterInput = document.getElementById('theater');
            if (theaterInput) {
                theaterInput.value = this.dataset.theater;
            }
            
            updateBookingSummary();
        });
    });
}

// Showtime Selection
function selectShowtime(button) {
    // Remove active class from all showtime buttons
    const showtimeBtns = document.querySelectorAll('.showtime-btn');
    showtimeBtns.forEach(btn => btn.classList.remove('active'));
    
    // Add active class to clicked button
    button.classList.add('active');
    
    // Update hidden input
    const showtimeInput = document.getElementById('showtime');
    if (showtimeInput) {
        showtimeInput.value = button.textContent.trim();
    }
    
    updateBookingSummary();
}

// Seat Selection
function initializeSeatSelection() {
    const seats = document.querySelectorAll('.seat:not(.occupied)');
    const selectedSeatsInput = document.getElementById('selected-seats');
    let selectedSeats = [];
    
    seats.forEach(seat => {
        seat.addEventListener('click', function() {
            const seatNumber = this.dataset.seat;
            
            if (this.classList.contains('selected')) {
                // Deselect seat
                this.classList.remove('selected');
                selectedSeats = selectedSeats.filter(s => s !== seatNumber);
            } else {
                // Select seat (limit to 10 seats)
                if (selectedSeats.length < 10) {
                    this.classList.add('selected');
                    selectedSeats.push(seatNumber);
                } else {
                    alert('Maximum 10 seats can be selected at once');
                }
            }
            
            // Update hidden input
            if (selectedSeatsInput) {
                selectedSeatsInput.value = selectedSeats.join(',');
            }
            
            // Update seat count display
            updateSeatCount(selectedSeats.length);
            updateBookingSummary();
        });
    });
}

function updateSeatCount(count) {
    const seatCountElement = document.getElementById('seat-count');
    if (seatCountElement) {
        seatCountElement.textContent = count;
    }
}

// Payment Method Selection
function initializePaymentSelection() {
    const paymentOptions = document.querySelectorAll('.payment-option');
    
    paymentOptions.forEach(option => {
        option.addEventListener('click', function() {
            // Remove selected class from all options
            paymentOptions.forEach(opt => opt.classList.remove('selected'));
            
            // Add selected class to clicked option
            this.classList.add('selected');
            
            // Update hidden input
            const paymentInput = document.getElementById('payment-method');
            if (paymentInput) {
                paymentInput.value = this.dataset.payment;
            }
            
            // Show/hide payment details based on selection
            showPaymentDetails(this.dataset.payment);
        });
    });
}

function showPaymentDetails(paymentMethod) {
    // Hide all payment detail sections
    const detailSections = document.querySelectorAll('.payment-details');
    detailSections.forEach(section => section.style.display = 'none');
    
    // Show selected payment detail section
    const selectedSection = document.getElementById(paymentMethod + '-details');
    if (selectedSection) {
        selectedSection.style.display = 'block';
    }
}

// Booking Summary Update
function updateBookingSummary() {
    const theater = document.getElementById('theater')?.value;
    const showtime = document.getElementById('showtime')?.value;
    const seats = document.getElementById('selected-seats')?.value;
    const ticketPrice = 12.00; // Default ticket price
    
    if (seats) {
        const seatCount = seats.split(',').length;
        const totalPrice = (seatCount * ticketPrice).toFixed(2);
        
        // Update summary display
        const summaryElement = document.getElementById('booking-summary');
        if (summaryElement) {
            summaryElement.innerHTML = `
                <h5>Booking Summary</h5>
                <p><strong>Theater:</strong> ${theater || 'Not selected'}</p>
                <p><strong>Showtime:</strong> ${showtime || 'Not selected'}</p>
                <p><strong>Seats:</strong> ${seats}</p>
                <p><strong>Number of Tickets:</strong> ${seatCount}</p>
                <p><strong>Price per Ticket:</strong> $${ticketPrice.toFixed(2)}</p>
                <hr>
                <h4><strong>Total:</strong> $${totalPrice}</h4>
            `;
        }
        
        // Update total price input
        const totalInput = document.getElementById('total-price');
        if (totalInput) {
            totalInput.value = totalPrice;
        }
    }
}

// Star Rating System
function initializeStarRating() {
    const stars = document.querySelectorAll('.star-rating i');
    const ratingInput = document.getElementById('rating');
    
    stars.forEach((star, index) => {
        star.addEventListener('click', function() {
            const rating = index + 1;
            
            // Update hidden input
            if (ratingInput) {
                ratingInput.value = rating;
            }
            
            // Update star display
            stars.forEach((s, i) => {
                if (i < rating) {
                    s.classList.remove('far');
                    s.classList.add('fas');
                } else {
                    s.classList.remove('fas');
                    s.classList.add('far');
                }
            });
        });
        
        // Hover effect
        star.addEventListener('mouseenter', function() {
            stars.forEach((s, i) => {
                if (i <= index) {
                    s.style.color = '#ffed4e';
                }
            });
        });
        
        star.addEventListener('mouseleave', function() {
            stars.forEach(s => {
                s.style.color = '#ffc107';
            });
        });
    });
}

// Form Validation
function validateBookingForm() {
    const theater = document.getElementById('theater')?.value;
    const showtime = document.getElementById('showtime')?.value;
    const seats = document.getElementById('selected-seats')?.value;
    
    if (!theater) {
        alert('Please select a theater');
        return false;
    }
    
    if (!showtime) {
        alert('Please select a showtime');
        return false;
    }
    
    if (!seats) {
        alert('Please select at least one seat');
        return false;
    }
    
    return true;
}

function validatePaymentForm() {
    const paymentMethod = document.getElementById('payment-method')?.value;
    
    if (!paymentMethod) {
        alert('Please select a payment method');
        return false;
    }
    
    return true;
}

// Search functionality
function performSearch() {
    const searchInput = document.getElementById('search-input');
    if (searchInput && searchInput.value.trim()) {
        window.location.href = `/search?q=${encodeURIComponent(searchInput.value)}`;
    }
}

// Auto-dismiss alerts after 5 seconds
setTimeout(function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        const bsAlert = new bootstrap.Alert(alert);
        bsAlert.close();
    });
}, 5000);

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Print ticket functionality
function printTicket() {
    window.print();
}

// Download ticket as PDF (basic implementation)
function downloadTicket() {
    alert('Ticket download will be available soon!');
    // In a real implementation, you would integrate with a PDF library like jsPDF
}

// Confirm before deleting
function confirmDelete(itemName) {
    return confirm(`Are you sure you want to delete ${itemName}? This action cannot be undone.`);
}

// Loading spinner
function showLoadingSpinner() {
    const spinner = document.createElement('div');
    spinner.id = 'loading-spinner';
    spinner.className = 'position-fixed top-50 start-50 translate-middle';
    spinner.innerHTML = '<div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div>';
    document.body.appendChild(spinner);
}

function hideLoadingSpinner() {
    const spinner = document.getElementById('loading-spinner');
    if (spinner) {
        spinner.remove();
    }
}

// Format currency
function formatCurrency(amount) {
    return '$' + parseFloat(amount).toFixed(2);
}

// Countdown timer for upcoming movies
function initializeCountdown() {
    const countdownElements = document.querySelectorAll('[data-countdown]');
    
    countdownElements.forEach(element => {
        const targetDate = new Date(element.dataset.countdown).getTime();
        
        const updateCountdown = () => {
            const now = new Date().getTime();
            const distance = targetDate - now;
            
            if (distance < 0) {
                element.innerHTML = 'Released!';
                return;
            }
            
            const days = Math.floor(distance / (1000 * 60 * 60 * 24));
            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);
            
            element.innerHTML = `${days}d ${hours}h ${minutes}m ${seconds}s`;
        };
        
        updateCountdown();
        setInterval(updateCountdown, 1000);
    });
}

// Initialize countdown if elements exist
if (document.querySelectorAll('[data-countdown]').length > 0) {
    initializeCountdown();
}