// AI Legal Document Assistant - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

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

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Add loading state to forms
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
                
                // Re-enable button after 10 seconds as fallback
                setTimeout(function() {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalText;
                }, 10000);
            }
        });
    });

    // File upload drag and drop enhancement
    const uploadAreas = document.querySelectorAll('.upload-area');
    uploadAreas.forEach(function(area) {
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            area.addEventListener(eventName, preventDefaults, false);
        });

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        ['dragenter', 'dragover'].forEach(eventName => {
            area.addEventListener(eventName, highlight, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            area.addEventListener(eventName, unhighlight, false);
        });

        function highlight(e) {
            area.classList.add('drag-over');
        }

        function unhighlight(e) {
            area.classList.remove('drag-over');
        }
    });

    // Copy to clipboard functionality
    window.copyToClipboard = function(text) {
        navigator.clipboard.writeText(text).then(function() {
            // Show success message
            const toast = document.createElement('div');
            toast.className = 'toast align-items-center text-white bg-success border-0';
            toast.setAttribute('role', 'alert');
            toast.innerHTML = `
                <div class="d-flex">
                    <div class="toast-body">
                        <i class="fas fa-check me-2"></i>Copied to clipboard!
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
                </div>
            `;
            
            document.body.appendChild(toast);
            const bsToast = new bootstrap.Toast(toast);
            bsToast.show();
            
            // Remove toast element after it's hidden
            toast.addEventListener('hidden.bs.toast', function() {
                document.body.removeChild(toast);
            });
        }).catch(function(err) {
            console.error('Could not copy text: ', err);
        });
    };

    // Search functionality
    window.performSearch = function(query) {
        if (!query.trim()) return;
        
        const searchResults = document.getElementById('searchResults');
        if (searchResults) {
            searchResults.innerHTML = '<div class="text-center"><div class="spinner-border" role="status"></div></div>';
            
            // Simulate search (replace with actual API call)
            setTimeout(function() {
                searchResults.innerHTML = '<div class="alert alert-info">Search functionality will be implemented with the legal search API.</div>';
            }, 1000);
        }
    };

    // Document processing status checker
    window.checkProcessingStatus = function(documentId) {
        fetch(`/documents/process/${documentId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.reload();
            }
        })
        .catch(error => {
            console.error('Error checking processing status:', error);
        });
    };

    // Auto-refresh for processing documents
    const processingElements = document.querySelectorAll('[data-processing="true"]');
    processingElements.forEach(function(element) {
        const documentId = element.dataset.documentId;
        if (documentId) {
            const interval = setInterval(function() {
                fetch(`/documents/process/${documentId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({})
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        clearInterval(interval);
                        window.location.reload();
                    }
                })
                .catch(error => {
                    console.error('Error checking processing status:', error);
                });
            }, 5000);
        }
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + K for search
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.querySelector('input[type="search"]');
            if (searchInput) {
                searchInput.focus();
            }
        }
        
        // Escape to close modals
        if (e.key === 'Escape') {
            const modals = document.querySelectorAll('.modal.show');
            modals.forEach(function(modal) {
                const bsModal = bootstrap.Modal.getInstance(modal);
                if (bsModal) {
                    bsModal.hide();
                }
            });
        }
    });

    // Form validation enhancement
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Lazy loading for images
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });

        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }

    // Print functionality
    window.printDocument = function() {
        window.print();
    };

    // Export functionality
    window.exportDocument = function(format) {
        const documentId = document.querySelector('[data-document-id]')?.dataset.documentId;
        if (documentId) {
            window.location.href = `/documents/download/${documentId}/${format}/`;
        }
    };

    // Initialize animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
            }
        });
    }, observerOptions);

    document.querySelectorAll('.card, .feature-card, .step-card').forEach(el => {
        observer.observe(el);
    });
});

// Utility functions
window.utils = {
    formatFileSize: function(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },
    
    formatDate: function(date) {
        return new Date(date).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    },
    
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
};




