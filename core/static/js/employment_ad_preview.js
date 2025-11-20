

// ===== Script // Script 1 =====

// Script 2


          // Simple interview section styling - clean and minimal
          function normalizeInterviewSectionStyling() {
            const interviewSection = document.querySelector('.interview-section');
            const interviewDateTextElement = document.getElementById('interview-date-text');
            
            if (interviewSection && interviewDateTextElement) {
              // Apply consistent styling to the interview text
              interviewDateTextElement.style.setProperty('font-weight', '900', 'important');
              interviewDateTextElement.style.setProperty('font-family', '"Arial Black", "Arial", "Noto Sans Devanagari", "Hind", sans-serif', 'important');
              interviewDateTextElement.style.setProperty('text-align', 'center', 'important');
              
              console.log('Applied clean styling to interview section');
            }
          }
          
          // Call the normalization function when page loads
          document.addEventListener('DOMContentLoaded', function() {
            normalizeInterviewSectionStyling();
          });
          
          // Handle company name alignment
          function adjustCompanyNameAlignment() {
            const companyRow = document.getElementById('company-row');
            if (companyRow) {
              // Check if the text content is too long (more than 30 characters)
              const companyText = companyRow.textContent;
              if (companyText.length > 30) {
                companyRow.classList.add('long-name');
              } else {
                companyRow.classList.remove('long-name');
              }
            }
          }
          
          // Call the function when page loads
          document.addEventListener('DOMContentLoaded', adjustCompanyNameAlignment);
          
          // Handle city field alignment
          function adjustCityAlignment() {
            const cityItem = document.getElementById('city-item');
            const metaItemsRow = document.getElementById('meta-items-row');
            
            if (cityItem && metaItemsRow) {
              // Check if the city text content is too long (more than 12 characters)
              const cityText = cityItem.textContent;
              console.log('City text:', cityText, 'Length:', cityText.length);
              if (cityText.length > 12) {
                cityItem.classList.add('long-city');
                metaItemsRow.classList.add('long-city');
                // Apply smaller font size to city item
                cityItem.style.fontSize = '3pt';
                console.log('Added long-city class to city item and meta row, reduced font size');
              } else {
                cityItem.classList.remove('long-city');
                metaItemsRow.classList.remove('long-city');
                // Reset font size to normal
                cityItem.style.fontSize = '4pt';
                console.log('Removed long-city class from city item and meta row, reset font size');
              }
            }
          }
          
          // Call the function when page loads
          document.addEventListener('DOMContentLoaded', adjustCityAlignment);
          
          // Force left alignment for ALL extra-note content
          function handleJapanContent() {
            const extraNote = document.querySelector('.extra-note');
            if (extraNote) {
              // Simple and direct - force left alignment on everything
              extraNote.style.setProperty('text-align', 'left', 'important');
              extraNote.style.setProperty('text-justify', 'initial', 'important');
              
              // Format bold elements properly
              const boldElements = extraNote.querySelectorAll('b, strong');
              boldElements.forEach(function(bold) {
                bold.style.setProperty('font-weight', 'bold', 'important');
                bold.style.setProperty('display', 'block', 'important');
                bold.style.setProperty('margin-bottom', '4px', 'important');
                bold.style.setProperty('text-align', 'left', 'important');
              });
              
              // Format paragraphs properly
              const paragraphs = extraNote.querySelectorAll('p');
              paragraphs.forEach(function(p) {
                p.style.setProperty('display', 'block', 'important');
                p.style.setProperty('margin-bottom', '8px', 'important');
                p.style.setProperty('text-align', 'left', 'important');
                p.style.setProperty('line-height', '1.4', 'important');
                p.style.setProperty('font-weight', 'normal', 'important');
                
                // Format bold elements within paragraphs
                const boldElements = p.querySelectorAll('b, strong');
                boldElements.forEach(function(bold) {
                  bold.style.setProperty('font-weight', 'bold', 'important');
                  bold.style.setProperty('display', 'inline', 'important');
                  bold.style.setProperty('margin-bottom', '0', 'important');
                });
              });
              
              // Force left alignment on all other elements
              const allElements = extraNote.querySelectorAll('*');
              allElements.forEach(function(element) {
                element.style.setProperty('text-align', 'left', 'important');
                element.style.setProperty('text-justify', 'initial', 'important');
              });
              
              console.log('Applied left alignment to all extra-note content');
            }
          }
          
          // Call the function when page loads
          document.addEventListener('DOMContentLoaded', handleJapanContent);
          
          // Ensure each data row is strictly 0.18cm (reduced by 2mm)
          function adjustTbodyHeight() {
            const tbody = document.querySelector('.main-table tbody');
            if (tbody) {
              const dataRows = tbody.querySelectorAll('.data-row');
              console.log('Found', dataRows.length, 'data rows');
              
              // Allow tbody to grow naturally
              tbody.style.setProperty('height', 'auto', 'important');
              tbody.style.setProperty('min-height', 'auto', 'important');
              tbody.style.setProperty('max-height', 'none', 'important');
              
              // Set each row to strictly 0.18cm with no padding/margin (reduced by 2mm)
              dataRows.forEach((row, index) => {
                // Use cssText to completely override any existing styles
                row.style.cssText += 'height: 0.18cm !important; min-height: 0.18cm !important; max-height: 0.18cm !important; margin: 0px !important; padding: 0px !important;';
                row.style.setProperty('height', '0.18cm', 'important');
                row.style.setProperty('min-height', '0.18cm', 'important');
                row.style.setProperty('max-height', '0.18cm', 'important');
                row.style.setProperty('margin', '0px', 'important');
                row.style.setProperty('padding', '0px', 'important');
                console.log('Set row', index, 'height to 0.18cm');
                
                // Set each cell in the row to 0.18cm with no padding/margin (reduced by 2mm)
                const cells = row.querySelectorAll('td');
                cells.forEach((cell, cellIndex) => {
                  // Use cssText to completely override any existing styles
                  cell.style.cssText += 'height: 0.18cm !important; min-height: 0.18cm !important; max-height: 0.18cm !important;';
                  cell.style.setProperty('height', '0.18cm', 'important');
                  cell.style.setProperty('min-height', '0.18cm', 'important');
                  cell.style.setProperty('max-height', '0.18cm', 'important');
                  cell.style.setProperty('overflow', 'hidden', 'important');
                  cell.style.setProperty('line-height', '1.0', 'important');
                  cell.style.setProperty('padding', '0px', 'important');
                  cell.style.setProperty('margin', '0px', 'important');
                  cell.style.setProperty('border-spacing', '0px', 'important');
                  console.log('Set cell', cellIndex, 'height to 0.18cm');
                  
                  // Don't override font-size for position field (text-left class), min_qualification field (text-center class), or hours/days cells
                  if (!cell.classList.contains('text-left') && !cell.classList.contains('text-center') && !cell.classList.contains('col-hours') && !cell.classList.contains('col-days')) {
                    cell.style.setProperty('font-size', '6.5pt', 'important');
                  }
                  
                  // Ensure position field has correct font size and styling
                  if (cell.classList.contains('text-left')) {
                    cell.style.setProperty('font-size', '7pt', 'important');
                    cell.style.setProperty('font-weight', '400', 'important');
                    cell.style.setProperty('padding-left', '2px', 'important');
                  }
                  
                  // Ensure yearly leave column is centered
                  if (cell.classList.contains('col-leave')) {
                    cell.style.textAlign = 'center';
                    cell.setAttribute('style', cell.getAttribute('style') + '; text-align: center !important;');
                    cell.style.setProperty('font-size', '3.5pt', 'important'); /* Reduced by 0.5pt from 4pt */
                  }
                  
                  // Ensure overtime column is centered and has correct font size
                  if (cell.classList.contains('col-overtime')) {
                    cell.style.setProperty('text-align', 'center', 'important');
                    cell.style.setProperty('font-size', '3.5pt', 'important'); /* Reduced by 0.5pt from 4pt */
                  }
                  
                  // Ensure min_qualification field has correct font size and alignment
                  if (cell.classList.contains('text-center')) {
                    cell.style.setProperty('font-size', '3.5pt', 'important'); /* Reduced by 0.5pt from 4pt */
                    cell.style.setProperty('text-align', 'center', 'important');
                  }
                });
              });
            }
          }
          
          // Single initialization - no timeouts to prevent flickering
          document.addEventListener('DOMContentLoaded', function() {
            // Run all functions immediately without delays
            adjustTbodyHeight();
            
            // Run all other functions immediately - no timeouts
            handleJapanContent();
            adjustCityAlignment();
            adjustCompanyNameAlignment();
            
            // Only calculate interview date if there are calculation elements
            const hasCalculatedElements = document.getElementById('calculated-interview-date');
            if (hasCalculatedElements) {
              calculateInterviewDate();
            }
            
            // Run height adjustment again after other functions to ensure it's not overridden
            setTimeout(adjustTbodyHeight, 100);
            setTimeout(adjustTbodyHeight, 500);
            setTimeout(adjustTbodyHeight, 1000);
            
            // Show content only after everything is processed
            const employmentAd = document.querySelector('.employment-ad');
            if (employmentAd) {
              employmentAd.classList.add('loaded');
            }
          });
          
          // Production-ready font weight handler - prevents flickering
          let fontsProcessed = false;
          
          function forceLightFontWeights() {
            // Prevent multiple executions to avoid flickering
            if (fontsProcessed) {
              return;
            }
            
            // Force apply light font weights
            const extraTableCells = document.querySelectorAll('.extra-table th, .extra-table td');
            extraTableCells.forEach(function(cell) {
              if (!cell.dataset.fontProcessed) {
                cell.style.setProperty('font-weight', '100', 'important');
                cell.dataset.fontProcessed = 'true';
              }
            });
            
            const extraNoteElements = document.querySelectorAll('.extra-note, .extra-note h4, .notice-content');
            extraNoteElements.forEach(function(element) {
              // Skip Japan content - it has its own formatting
              if (element.classList.contains('japan-content')) {
                return;
              }
              
              if (!element.dataset.fontProcessed) {
                element.style.setProperty('font-weight', '200', 'important');
                element.style.setProperty('font-size', '3.56pt', 'important');
                element.style.setProperty('line-height', '1.4', 'important');
                element.style.setProperty('text-align', 'left', 'important');
                element.style.setProperty('text-justify', 'initial', 'important');
                element.style.setProperty('margin', '0px', 'important');
                element.style.setProperty('padding', '2px 4px', 'important');
                element.style.setProperty('display', 'block', 'important');
                element.style.setProperty('width', '100%', 'important');
                element.dataset.fontProcessed = 'true';
              }
            });
            
            // Handle Japan content formatting in print mode
            const japanContent = document.querySelector('.extra-note.japan-content');
            if (japanContent) {
              // Apply left alignment to the main container
              japanContent.style.setProperty('text-align', 'left', 'important');
              japanContent.style.setProperty('text-justify', 'initial', 'important');
              
              // Handle bold elements
              const boldElements = japanContent.querySelectorAll('b');
              boldElements.forEach(function(bold) {
                bold.style.setProperty('display', 'block', 'important');
                bold.style.setProperty('margin-bottom', '2px', 'important');
                bold.style.setProperty('font-weight', 'bold', 'important');
                bold.style.setProperty('text-align', 'left', 'important');
                bold.style.setProperty('text-justify', 'initial', 'important');
              });
              
              // Handle paragraphs
              const paragraphs = japanContent.querySelectorAll('p');
              paragraphs.forEach(function(p) {
                p.style.setProperty('display', 'block', 'important');
                p.style.setProperty('margin-bottom', '4px', 'important');
                p.style.setProperty('text-align', 'left', 'important');
                p.style.setProperty('text-justify', 'initial', 'important');
                p.style.setProperty('line-height', '1.2', 'important');
                p.style.setProperty('font-size', '3.56pt', 'important');
              });
            }
            
            // Also target all paragraphs within notice content
            const noticeParagraphs = document.querySelectorAll('.notice-content p, .notice-content div, .extra-note p, .extra-note div');
            noticeParagraphs.forEach(function(element) {
              // Check if this is Japan content
              const extraNote = element.closest('.extra-note');
              if (extraNote && extraNote.classList.contains('japan-content')) {
                element.style.setProperty('text-align', 'left', 'important');
                element.style.setProperty('text-justify', 'initial', 'important');
              } else {
                element.style.setProperty('text-align', 'justify', 'important');
                element.style.setProperty('text-justify', 'inter-word', 'important');
              }
              element.style.setProperty('font-size', '3.56pt', 'important');
              element.style.setProperty('line-height', '1.4', 'important');
              element.style.setProperty('width', 'auto', 'important');
              element.style.setProperty('max-width', '100%', 'important');
              element.style.setProperty('margin', '0px', 'important');
              element.style.setProperty('padding', '0px', 'important');
              element.style.setProperty('display', 'inline', 'important');
            });
            
            // Left align the note section (last bold element)
            const noteElement = document.querySelector('.extra-note b:last-child');
            if (noteElement) {
              noteElement.style.setProperty('text-align', 'left', 'important');
              noteElement.style.setProperty('display', 'inline', 'important');
              noteElement.style.setProperty('width', 'auto', 'important');
              noteElement.style.setProperty('padding', '0px', 'important');
              noteElement.style.setProperty('margin', '0px', 'important');
            }
            
            const mainTableCells = document.querySelectorAll('.main-table td.text-left');
            mainTableCells.forEach(function(cell) {
              cell.style.setProperty('font-family', "'Olympia-BoldCond', Arial, sans-serif", 'important');
              cell.style.setProperty('font-size', '8pt', 'important');
              cell.style.setProperty('line-height', '8pt', 'important');
              cell.style.setProperty('font-weight', '900', 'important');
              cell.style.setProperty('font-stretch', 'condensed', 'important');
              cell.style.setProperty('text-transform', 'uppercase', 'important');
              cell.style.setProperty('letter-spacing', '0', 'important');
              cell.style.setProperty('font-kerning', 'auto', 'important');
              cell.style.setProperty('text-rendering', 'optimizeLegibility', 'important');
              cell.style.setProperty('-webkit-font-smoothing', 'antialiased', 'important');
              cell.style.setProperty('-moz-osx-font-smoothing', 'grayscale', 'important');
            });
            
            const centerCells = document.querySelectorAll('.main-table .text-center, .main-table td.col-leave, .main-table td.col-overtime');
            centerCells.forEach(function(cell) {
              cell.style.setProperty('font-weight', '200', 'important');
              cell.style.fontWeight = '200';
              cell.setAttribute('style', cell.getAttribute('style') + '; font-weight: 200 !important;');
            });
            
            // Apply Olympia font to specific data cells
            const olympiaDataCells = document.querySelectorAll('.main-table .olympia-data');
            olympiaDataCells.forEach(function(cell) {
              cell.style.setProperty('font-family', "'Olympia-BoldCond', Arial, sans-serif", 'important');
              cell.style.setProperty('font-size', '6.5pt', 'important');
              cell.style.setProperty('line-height', '6.5pt', 'important');
              cell.style.setProperty('font-weight', '900', 'important');
              cell.style.setProperty('font-stretch', 'condensed', 'important');
              cell.style.setProperty('text-transform', 'uppercase', 'important');
              cell.style.setProperty('letter-spacing', '0', 'important');
              cell.style.setProperty('font-kerning', 'auto', 'important');
              cell.style.setProperty('text-rendering', 'optimizeLegibility', 'important');
              cell.style.setProperty('-webkit-font-smoothing', 'antialiased', 'important');
              cell.style.setProperty('-moz-osx-font-smoothing', 'grayscale', 'important');
              cell.style.setProperty('font-synthesis', 'none', 'important');
              cell.style.setProperty('-webkit-text-stroke', '0.01em transparent', 'important');
              cell.style.setProperty('text-align', 'center', 'important');
            });
            
            // Header-left with InDesign specifications and GANESH font conversion
            document.addEventListener('DOMContentLoaded', function() {
            const headerLeft = document.querySelectorAll('.header-left');
            
            // GANESH font specific character mapping (based on actual font encoding)
            function convertToGaneshLayout(text) {
              // GANESH font uses specific character codes for Devanagari
              // This mapping is based on the actual GANESH.TTF font encoding
              const devanagariToGanesh = {
                // Complete words first (to avoid partial replacements)
                'मा रोजगारी': 'ma rojagari',
                'देश': 'desh',
                'कम्पनी': 'kampani',
                'जानकारी': 'jankari',
                'कुनै': 'kunai',
                'मिति': 'miti',
                'नम्बर': 'nambar',
                'शहर': 'sahar',
                'काम': 'kam',
                'सेवा': 'sewa',
                'विभाग': 'vibhag',
                'कार्यालय': 'karyalaya',
                'सम्पर्क': 'sampark',
                'फोन': 'phone',
                'ईमेल': 'email',
                'वेबसाइट': 'website',
                'पता': 'pata',
                
                // Individual characters (GANESH font specific mapping)
                'अ': 'a', 'आ': 'aa', 'इ': 'i', 'ई': 'ii', 'उ': 'u', 'ऊ': 'uu', 'ए': 'e', 'ऐ': 'ai', 'ओ': 'o', 'औ': 'au',
                'ा': 'aa', 'ि': 'i', 'ी': 'ii', 'ु': 'u', 'ू': 'uu', 'े': 'e', 'ै': 'ai', 'ो': 'o', 'ौ': 'au',
                'क': 'k', 'ख': 'kh', 'ग': 'g', 'घ': 'gh', 'ङ': 'ng',
                'च': 'c', 'छ': 'ch', 'ज': 'j', 'झ': 'jh', 'ञ': 'ny',
                'ट': 't', 'ठ': 'th', 'ड': 'd', 'ढ': 'dh', 'ण': 'n',
                'त': 't', 'थ': 'th', 'द': 'd', 'ध': 'dh', 'न': 'n',
                'प': 'p', 'फ': 'ph', 'ब': 'b', 'भ': 'bh', 'म': 'm',
                'य': 'y', 'र': 'r', 'ल': 'l', 'व': 'v', 'श': 'sh', 'ष': 'sh', 'स': 's', 'ह': 'h',
                
                // Punctuation and symbols
                ' ': ' ', '।': '.', '?': '?', '!': '!', ':': ':', ';': ';',
                ',': ',', '.': '.', '-': '-', '–': '-', '—': '-',
                '०': '0', '१': '1', '२': '2', '३': '3', '४': '4',
                '५': '5', '६': '6', '७': '7', '८': '8', '९': '9'
              };
              
              let convertedText = text;
              
              // Replace complete words/phrases first
              for (const [devanagari, ganesh] of Object.entries(devanagariToGanesh)) {
                if (devanagari.length > 1) {
                  convertedText = convertedText.replace(new RegExp(devanagari, 'g'), ganesh);
                }
              }
              
              // Then replace individual characters
              for (const [devanagari, ganesh] of Object.entries(devanagariToGanesh)) {
                if (devanagari.length === 1) {
                  convertedText = convertedText.replace(new RegExp(devanagari, 'g'), ganesh);
                }
              }
              
              return convertedText;
            }
            
            // Function to apply Kalimati font with proper loading
            function applyKalimatiFont() {
            headerLeft.forEach(function(element) {
                // Apply Kalimati font directly (no text conversion needed for Unicode)
                element.style.setProperty('text-align', 'center', 'important');
                element.style.setProperty('font-family', 'Arial Black, Arial, Kalimati, Kalimati-Fallback, Noto Sans Devanagari, Hind, sans-serif', 'important');
                element.style.setProperty('font-size', '7pt', 'important');
                element.style.setProperty('line-height', '0.4cm', 'important');
                element.style.setProperty('font-weight', '900', 'important');
                element.style.setProperty('font-weight', 'bold', 'important');
                element.style.setProperty('text-shadow', '0.3px 0 0 currentColor, -0.3px 0 0 currentColor, 0 0.3px 0 currentColor, 0 -0.3px 0 currentColor', 'important');
                element.style.setProperty('-webkit-text-stroke', '0.01em black', 'important');
                element.style.setProperty('font-style', 'normal', 'important');
                element.style.setProperty('letter-spacing', '0.05em', 'important');
                element.style.setProperty('word-spacing', '0.1em', 'important');
                element.style.setProperty('text-rendering', 'optimizeLegibility', 'important');
                element.style.setProperty('-webkit-font-smoothing', 'antialiased', 'important');
                element.style.setProperty('-moz-osx-font-smoothing', 'grayscale', 'important');
                
                // Ensure text is not converted - keep original text
                const originalText = element.textContent;
                if (originalText && originalText !== element.textContent) {
                  element.textContent = originalText;
                }
              });
              
            }
            
            // Detect Safari browser
            function isSafari() {
              return /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
            }
            
            // Force Kalimati font loading
            window.forceKalimatiFont = function() {
              const fontFamily = 'Kalimati, Kalimati-Fallback, Noto Sans Devanagari, Hind, Arial, sans-serif';
              
              // Create a hidden element to force font loading
              const testElement = document.createElement('div');
              testElement.style.fontFamily = fontFamily;
              testElement.style.position = 'absolute';
              testElement.style.left = '-9999px';
              testElement.style.visibility = 'hidden';
              testElement.style.fontSize = '15pt';
              testElement.textContent = 'मा रोजगारी';
              document.body.appendChild(testElement);
              
              // Force font loading by measuring
              const canvas = document.createElement('canvas');
              const context = canvas.getContext('2d');
              context.font = '15pt ' + fontFamily;
              context.measureText('मा रोजगारी');
              
              // Preload Kalimati font
              const link = document.createElement('link');
              link.rel = 'preload';
              link.as = 'font';
              link.type = 'font/ttf';
              link.href = '{{ STATIC_URL }}fonts/Kalimati.ttf';
              link.crossOrigin = 'anonymous';
              document.head.appendChild(link);
              
              // Clean up
              document.body.removeChild(testElement);
              
              console.log('Kalimati font forced to load');
              return true;
            }
            
            // Debug: Check if elements exist
            console.log('Header elements found:', headerLeft.length);
            
            if (headerLeft.length === 0) {
              console.log('No header-left elements found, retrying...');
              setTimeout(function() {
                const retryElements = document.querySelectorAll('.header-left');
                console.log('Retry - Header elements found:', retryElements.length);
                if (retryElements.length > 0) {
                  headerLeft = retryElements;
                  if (typeof forceKalimatiFont === 'function') {
                    forceKalimatiFont();
                  }
                  if (typeof applyKalimatiFont === 'function') {
                    applyKalimatiFont();
                  }
                }
              }, 100);
            } else {
            // Force Kalimati font loading and apply
            if (typeof forceKalimatiFont === 'function') {
              forceKalimatiFont();
            }
            if (typeof applyKalimatiFont === 'function') {
              applyKalimatiFont();
            }
            }
            
            // Reapply multiple times to ensure proper rendering
            setTimeout(function() {
              console.log('Reapplying Kalimati font...');
              applyKalimatiFont();
            }, 500);
            
            setTimeout(function() {
              console.log('Final Kalimati font application...');
              applyKalimatiFont();
            }, 1500);
            
            // Additional debugging - check font loading
            setTimeout(function() {
              const testDiv = document.createElement('div');
              testDiv.style.fontFamily = 'Kalimati';
              testDiv.style.fontSize = '15pt';
              testDiv.textContent = 'मा रोजगारी';
              testDiv.style.position = 'absolute';
              testDiv.style.left = '-9999px';
              document.body.appendChild(testDiv);
              
              const computedStyle = window.getComputedStyle(testDiv);
              console.log('GANESH font computed:', computedStyle.fontFamily);
              console.log('GANESH font size:', computedStyle.fontSize);
              
              document.body.removeChild(testDiv);
            }, 2000);
            
            }); // End of DOMContentLoaded
            
            // Fallback: Run immediately if DOM is already loaded
            if (document.readyState === 'loading') {
              // DOM is still loading, DOMContentLoaded will handle it
            } else {
              // DOM is already loaded, run immediately
              const headerLeft = document.querySelectorAll('.header-left');
              if (headerLeft.length > 0) {
                console.log('DOM already loaded, running Kalimati font immediately');
                if (typeof forceKalimatiFont === 'function') {
                  forceKalimatiFont();
                }
                if (typeof applyKalimatiFont === 'function') {
                  applyKalimatiFont();
                }
              }
            }
            
            const headerRight = document.querySelectorAll('.header-right');
            headerRight.forEach(function(element) {
              element.style.setProperty('position', 'absolute', 'important');
              element.style.setProperty('right', '6px', 'important');
              element.style.setProperty('top', '50%', 'important');
              element.style.setProperty('transform', 'translateY(-50%)', 'important');
              element.style.setProperty('font-family', '"Roboto", Arial, sans-serif', 'important');
              element.style.setProperty('font-size', '6pt', 'important');
              element.style.setProperty('font-weight', '700', 'important');
              element.style.setProperty('line-height', '4.5pt', 'important');
              element.style.setProperty('letter-spacing', '0', 'important');
              element.style.setProperty('text-rendering', 'optimizeLegibility', 'important');
              element.style.setProperty('-webkit-font-smoothing', 'antialiased', 'important');
              element.style.setProperty('-moz-osx-font-smoothing', 'grayscale', 'important');
              element.style.setProperty('font-synthesis', 'none', 'important');
              element.style.setProperty('-webkit-text-stroke', '0.01em transparent', 'important');
              element.style.setProperty('text-align', 'right', 'important');
            });
            
            // Apply Kalimati font to interview section - ALLOW MULTIPLE LINES
            const interviewSections = document.querySelectorAll('.interview-section');
            interviewSections.forEach(function(element) {
              element.style.setProperty('background', '#000', 'important');
              element.style.setProperty('color', '#fff', 'important');
              element.style.setProperty('padding', '0.02cm 0.1cm', 'important'); // Minimal vertical padding
              element.style.setProperty('margin', '0px', 'important');
              element.style.setProperty('margin-bottom', '0px', 'important');
              element.style.setProperty('border', 'none', 'important');
              element.style.setProperty('text-align', 'center', 'important');
              // ALLOW MULTIPLE LINES - allow expansion when custom text is entered
              element.style.setProperty('height', 'auto', 'important');
              element.style.setProperty('min-height', 'auto', 'important'); // No minimum height - fit content exactly
              element.style.setProperty('max-height', 'none', 'important');
              element.style.setProperty('overflow', 'visible', 'important');
              element.style.setProperty('white-space', 'normal', 'important');
              element.style.setProperty('word-wrap', 'break-word', 'important');
              element.style.setProperty('overflow-wrap', 'break-word', 'important');
              element.style.setProperty('display', 'block', 'important'); // Changed from flex to block
              element.style.setProperty('box-sizing', 'border-box', 'important');
              element.style.setProperty('position', 'relative', 'important');
              element.style.setProperty('isolation', 'isolate', 'important');
              element.style.setProperty('contain', 'layout style', 'important'); // Removed 'size' to allow growth
              element.style.setProperty('text-overflow', 'initial', 'important'); // NO ELLIPSIS
              element.style.setProperty('font-family', '"Arial Black", "Arial", "Noto Sans Devanagari", "Hind", sans-serif', 'important');
              element.style.setProperty('font-size', '7pt', 'important');
              element.style.setProperty('font-weight', '900', 'important');
              element.style.setProperty('font-weight', 'bold', 'important'); // Fallback
              element.style.setProperty('line-height', '1.2', 'important'); // Allow line spacing
              element.style.setProperty('letter-spacing', '-0.05em', 'important'); /* Tracking: -5 */
              element.style.setProperty('font-kerning', 'auto', 'important'); /* Kerning: Metrics */
              element.style.setProperty('text-rendering', 'optimizeLegibility', 'important');
              element.style.setProperty('-webkit-font-smoothing', 'antialiased', 'important');
              element.style.setProperty('-moz-osx-font-smoothing', 'grayscale', 'important');
              element.style.setProperty('font-synthesis', 'none', 'important');
              element.style.setProperty('-webkit-text-stroke', '0.01em transparent', 'important');
              
              // Also make all child elements bold and allow wrapping
              const childElements = element.querySelectorAll('*');
              childElements.forEach(function(child) {
                // Skip br tags - they need special handling
                if (child.tagName === 'BR') {
                  return;
                }
                child.style.setProperty('font-weight', '900', 'important');
                child.style.setProperty('font-weight', 'bold', 'important');
                child.style.setProperty('font-family', '"Arial Black", "Arial", "Noto Sans Devanagari", "Hind", sans-serif', 'important');
                // Allow child elements to wrap and preserve line breaks
                child.style.setProperty('overflow', 'visible', 'important');
                child.style.setProperty('white-space', 'pre-wrap', 'important'); // Preserve line breaks and wrap
                child.style.setProperty('word-wrap', 'break-word', 'important');
                child.style.setProperty('overflow-wrap', 'break-word', 'important');
                child.style.setProperty('max-width', '100%', 'important');
                child.style.setProperty('width', '100%', 'important');
                child.style.setProperty('text-align', 'center', 'important');
                child.style.setProperty('line-height', '1.2', 'important'); // Tighter line height
                child.style.setProperty('box-sizing', 'border-box', 'important');
              });
              
              // Specifically handle the interview text content - ALLOW MULTIPLE LINES
              const interviewText = element.querySelector('#interview-date-text');
              if (interviewText) {
                // Check if it's manual custom text (has interview-custom-text-content class)
                if (interviewText.classList.contains('interview-custom-text-content')) {
                  // Manual text - apply pre-wrap styling
                  interviewText.style.setProperty('overflow', 'visible', 'important');
                  interviewText.style.setProperty('white-space', 'pre-wrap', 'important'); // Preserve line breaks and wrap
                  interviewText.style.setProperty('word-wrap', 'break-word', 'important');
                  interviewText.style.setProperty('overflow-wrap', 'break-word', 'important');
                  interviewText.style.setProperty('max-width', '100%', 'important');
                  interviewText.style.setProperty('width', '100%', 'important');
                  interviewText.style.setProperty('display', 'block', 'important');
                  interviewText.style.setProperty('text-align', 'center', 'important');
                  interviewText.style.setProperty('line-height', '1.2', 'important'); // Tighter line height
                  interviewText.style.setProperty('box-sizing', 'border-box', 'important');
                  interviewText.style.setProperty('margin', '0', 'important');
                  interviewText.style.setProperty('padding', '0', 'important'); // No padding on text
                } else {
                  // Automatic text - just ensure it's styled correctly
                  interviewText.style.setProperty('display', 'block', 'important');
                  interviewText.style.setProperty('text-align', 'center', 'important');
                  interviewText.style.setProperty('margin', '0', 'important');
                  interviewText.style.setProperty('padding', '0', 'important');
                }
              }
              
              // Handle custom text content specifically - ALLOW MULTIPLE LINES
              // Now the custom text is directly in #interview-date-text with class interview-custom-text-content
              const customTextContent = element.querySelector('#interview-date-text.interview-custom-text-content');
              if (customTextContent) {
                // Force white-space to pre-wrap to preserve line breaks
                customTextContent.style.cssText = 'white-space: pre-wrap !important; word-wrap: break-word !important; overflow-wrap: break-word !important; display: block !important; width: 100% !important; max-width: 100% !important; text-align: center !important; margin: 0 !important; padding: 0 !important; background: transparent !important; border: none !important; font-family: "Arial Black", Arial, "Noto Sans Devanagari", Hind, sans-serif !important; font-weight: 900 !important; font-size: 7pt !important; line-height: 1.2 !important; box-sizing: border-box !important; overflow: visible !important; height: auto !important; min-height: auto !important; max-height: none !important; text-overflow: initial !important;';
                
                // Also set individually to ensure they stick
                customTextContent.style.setProperty('white-space', 'pre-wrap', 'important');
                customTextContent.style.setProperty('word-wrap', 'break-word', 'important');
                customTextContent.style.setProperty('overflow-wrap', 'break-word', 'important');
                customTextContent.style.setProperty('display', 'block', 'important');
                customTextContent.style.setProperty('width', '100%', 'important');
                customTextContent.style.setProperty('max-width', '100%', 'important');
                customTextContent.style.setProperty('text-align', 'center', 'important');
                customTextContent.style.setProperty('overflow', 'visible', 'important');
                customTextContent.style.setProperty('height', 'auto', 'important');
                customTextContent.style.setProperty('min-height', 'auto', 'important');
                customTextContent.style.setProperty('max-height', 'none', 'important');
                customTextContent.style.setProperty('text-overflow', 'initial', 'important'); // NO ELLIPSIS
                
                // Debug: log the content to see if newlines are present
                console.log('Interview custom text content:', customTextContent.textContent);
                console.log('Interview custom text innerHTML:', customTextContent.innerHTML);
                console.log('Has newlines:', customTextContent.textContent.includes('\n'));
                console.log('Computed white-space:', window.getComputedStyle(customTextContent).whiteSpace);
                console.log('Computed overflow:', window.getComputedStyle(customTextContent).overflow);
                console.log('Computed text-overflow:', window.getComputedStyle(customTextContent).textOverflow);
              }
            });
            
            // DISABLED: AGGRESSIVE INTERVIEW SECTION STYLING - was causing layout conflicts
            /*
            function forceInterviewSectionStyling() {
              // Disabled to prevent layout conflicts with manual text
            }
            
            // Run immediately
            forceInterviewSectionStyling();
            
            // Run again after a short delay
            setTimeout(forceInterviewSectionStyling, 100);
            setTimeout(forceInterviewSectionStyling, 500);
            setTimeout(forceInterviewSectionStyling, 1000);
            */
            
            // Also try with different selectors in case the class name is different
            // DISABLED: Alternative aggressive styling - was causing layout conflicts
            /*
            function forceInterviewSectionStylingAlternative() {
              // Disabled to prevent layout conflicts with manual text
            }
            
            // Run alternative approach
            setTimeout(forceInterviewSectionStylingAlternative, 200);
            setTimeout(forceInterviewSectionStylingAlternative, 1200);
            */
            
            // Debug function to check interview section styling
            function debugInterviewSection() {
              console.log('=== DEBUGGING INTERVIEW SECTION ===');
              const interviewSections = document.querySelectorAll('.interview-section');
              console.log('Found interview sections:', interviewSections.length);
              
              if (interviewSections.length === 0) {
                console.log('NO INTERVIEW SECTIONS FOUND!');
                console.log('Looking for any elements with "interview" in class name...');
                const allElements = document.querySelectorAll('*');
                allElements.forEach(function(el) {
                  if (el.className && el.className.includes('interview')) {
                    console.log('Found element with interview in class:', el, el.className);
                  }
                });
                return;
              }
              
              interviewSections.forEach(function(element, index) {
                const computedStyle = window.getComputedStyle(element);
                console.log(`Interview section ${index}:`, {
                  element: element,
                  textContent: element.textContent.substring(0, 50) + '...',
                  background: computedStyle.backgroundColor,
                  color: computedStyle.color,
                  textAlign: computedStyle.textAlign,
                  display: computedStyle.display,
                  alignItems: computedStyle.alignItems,
                  justifyContent: computedStyle.justifyContent
                });
              });
            }
            
            // Run debug after styling
            setTimeout(debugInterviewSection, 200);
            setTimeout(debugInterviewSection, 1200);
            
            // Function to apply company row styles
            function applyCompanyRowStyles() {
              // Company container
              const companyContainer = document.querySelectorAll('.company-container');
              console.log('Found company containers:', companyContainer.length);
              companyContainer.forEach(function(element) {
                element.style.setProperty('display', 'flex', 'important');
                element.style.setProperty('align-items', 'center', 'important');
                element.style.setProperty('height', '0.3cm', 'important');
                console.log('Applied styles to company container');
            });
            
            // Company row
            const companyRow = document.querySelectorAll('.company-row');
              console.log('Found company rows:', companyRow.length);
            companyRow.forEach(function(element) {
              element.style.setProperty('display', 'flex', 'important');
              element.style.setProperty('align-items', 'center', 'important');
              element.style.setProperty('justify-content', 'center', 'important');
                element.style.setProperty('padding', '0px 3px', 'important');
                element.style.setProperty('font-family', '"Lato", Arial, sans-serif', 'important');
                element.style.setProperty('font-size', '7pt', 'important');
                element.style.setProperty('line-height', '8pt', 'important');
                element.style.setProperty('font-weight', '400', 'important');
                element.style.setProperty('text-align', 'center', 'important');
                element.style.setProperty('height', '0.4cm', 'important');
                element.style.setProperty('min-height', '0.4cm', 'important');
                element.style.setProperty('max-height', '0.4cm', 'important');
                element.style.setProperty('border-bottom', 'none', 'important');
                element.style.setProperty('word-wrap', 'break-word', 'important');
                element.style.setProperty('overflow-wrap', 'break-word', 'important');
                element.style.setProperty('white-space', 'nowrap', 'important');
              element.style.setProperty('overflow', 'hidden', 'important');
              element.style.setProperty('text-overflow', 'ellipsis', 'important');
                element.style.setProperty('flex', '1', 'important');
                element.style.setProperty('text-rendering', 'optimizeLegibility', 'important');
                element.style.setProperty('-webkit-font-smoothing', 'antialiased', 'important');
                element.style.setProperty('-moz-osx-font-smoothing', 'grayscale', 'important');
                console.log('Applied Lato styles to company row:', element.textContent);
              });
              
              // Company label - Lato Regular
              const companyLabel = document.querySelectorAll('.company-label');
              companyLabel.forEach(function(element) {
                element.style.setProperty('font-family', '"Arial Black", "Arial", "Kalimati", "Kalimati-Fallback", "Noto Sans Devanagari", "Hind", sans-serif', 'important');
                element.style.setProperty('font-size', '7pt', 'important');
                element.style.setProperty('font-weight', '900', 'important');
                element.style.setProperty('font-weight', 'bold', 'important');
                element.style.setProperty('line-height', '8pt', 'important');
                element.style.setProperty('text-shadow', '0.5px 0 0 currentColor, -0.5px 0 0 currentColor, 0 0.5px 0 currentColor, 0 -0.5px 0 currentColor, 0.3px 0.3px 0 currentColor, -0.3px -0.3px 0 currentColor', 'important');
                element.style.setProperty('font-style', 'normal', 'important');
                element.style.setProperty('letter-spacing', '0.05em', 'important');
                element.style.setProperty('word-spacing', '0.1em', 'important');
                element.style.setProperty('text-rendering', 'optimizeLegibility', 'important');
                element.style.setProperty('-webkit-font-smoothing', 'antialiased', 'important');
                element.style.setProperty('-moz-osx-font-smoothing', 'grayscale', 'important');
                element.style.setProperty('font-synthesis', 'none', 'important');
                element.style.setProperty('-webkit-text-stroke', '0.01em black', 'important');
                element.style.setProperty('text-shadow', '0.3px 0.3px 0px rgba(0,0,0,0.2)', 'important');
                element.style.setProperty('font-style', 'normal', 'important');
                element.style.setProperty('letter-spacing', '0', 'important');
                element.style.setProperty('word-spacing', '0', 'important');
                element.style.setProperty('text-rendering', 'optimizeLegibility', 'important');
                element.style.setProperty('-webkit-font-smoothing', 'antialiased', 'important');
                element.style.setProperty('-moz-osx-font-smoothing', 'grayscale', 'important');
                console.log('Applied Lato Regular to company label');
              });
              
              // Lato Black text
              const latoBlackText = document.querySelectorAll('.lato-black-text');
              latoBlackText.forEach(function(element) {
                element.style.setProperty('font-family', '"Arial Black", "Arial", "Kalimati", "Kalimati-Fallback", "Noto Sans Devanagari", "Hind", sans-serif', 'important');
                element.style.setProperty('font-weight', '900', 'important');
                element.style.setProperty('font-weight', 'bold', 'important');
                element.style.setProperty('font-size', '7pt', 'important');
                element.style.setProperty('line-height', '8pt', 'important');
                element.style.setProperty('text-shadow', '0.5px 0 0 currentColor, -0.5px 0 0 currentColor, 0 0.5px 0 currentColor, 0 -0.5px 0 currentColor, 0.3px 0.3px 0 currentColor, -0.3px -0.3px 0 currentColor', 'important');
                element.style.setProperty('font-style', 'normal', 'important');
                element.style.setProperty('letter-spacing', '0.05em', 'important');
                element.style.setProperty('word-spacing', '0.1em', 'important');
                element.style.setProperty('text-rendering', 'optimizeLegibility', 'important');
                element.style.setProperty('-webkit-font-smoothing', 'antialiased', 'important');
                element.style.setProperty('-moz-osx-font-smoothing', 'grayscale', 'important');
                element.style.setProperty('font-synthesis', 'none', 'important');
                element.style.setProperty('-webkit-text-stroke', '0.01em black', 'important');
                element.style.setProperty('text-shadow', '0.3px 0.3px 0px rgba(0,0,0,0.2)', 'important');
                element.style.setProperty('letter-spacing', '0', 'important');
                element.style.setProperty('word-spacing', '0', 'important');
                element.style.setProperty('text-rendering', 'optimizeLegibility', 'important');
                element.style.setProperty('-webkit-font-smoothing', 'antialiased', 'important');
                element.style.setProperty('-moz-osx-font-smoothing', 'grayscale', 'important');
                console.log('Applied Lato Black to company name');
              });
            }
            
            // Apply styles immediately
            applyCompanyRowStyles();
            
            // Apply styles again after a short delay to ensure they stick
            setTimeout(applyCompanyRowStyles, 100);
            setTimeout(applyCompanyRowStyles, 500);
            
            // Additional debugging for company row
            console.log('Company row debugging:');
            const companyRowDebug = document.querySelectorAll('.company-row');
            companyRowDebug.forEach(function(element, index) {
              console.log('Company row', index, ':', element.textContent);
              console.log('Font family:', window.getComputedStyle(element).fontFamily);
              console.log('Font size:', window.getComputedStyle(element).fontSize);
              console.log('Font weight:', window.getComputedStyle(element).fontWeight);
            });
            
            // Meta bar - ensure it's isolated from interview section
            const metaBar = document.querySelectorAll('.meta-bar');
            metaBar.forEach(function(element) {
              element.style.setProperty('font-size', '5pt', 'important');
              element.style.setProperty('font-weight', '500', 'important');
              element.style.setProperty('height', '0.75cm', 'important');
              element.style.setProperty('max-height', '0.75cm', 'important');
              element.style.setProperty('min-height', '0.75cm', 'important');
              element.style.setProperty('overflow', 'hidden', 'important');
              element.style.setProperty('display', 'flex', 'important');
              element.style.setProperty('flex-direction', 'column', 'important');
              element.style.setProperty('padding-top', '0.08cm', 'important');
              element.style.setProperty('position', 'relative', 'important');
              element.style.setProperty('isolation', 'isolate', 'important');
              element.style.setProperty('contain', 'layout size style', 'important');
              element.style.setProperty('flex-shrink', '0', 'important');
              element.style.setProperty('flex-grow', '0', 'important');
              element.style.setProperty('margin-top', '0px', 'important');
              element.style.setProperty('margin-bottom', '0px', 'important');
            });
            
            // Meta items row
            const metaItemsRow = document.querySelectorAll('.meta-items-row');
            console.log('Found meta items rows:', metaItemsRow.length);
            metaItemsRow.forEach(function(element, index) {
              console.log('Applying styles to meta items row', index);
              element.style.setProperty('font-family', '"Roboto", Arial, sans-serif', 'important');
              element.style.setProperty('font-size', '6pt', 'important');
              element.style.setProperty('font-weight', '700', 'important');
              element.style.setProperty('line-height', '4.5pt', 'important');
              element.style.setProperty('letter-spacing', '0', 'important');
              element.style.setProperty('word-spacing', '0', 'important');
              element.style.setProperty('height', '0.3cm', 'important');
              element.style.setProperty('max-height', '0.3cm', 'important');
              element.style.setProperty('min-height', '0.3cm', 'important');
              element.style.setProperty('display', 'grid', 'important');
              element.style.setProperty('gap', '0.1cm', 'important');
              element.style.setProperty('margin-top', '0.05cm', 'important');
              element.style.setProperty('text-rendering', 'optimizeLegibility', 'important');
              element.style.setProperty('-webkit-font-smoothing', 'antialiased', 'important');
              element.style.setProperty('-moz-osx-font-smoothing', 'grayscale', 'important');
              
              // Adjust grid columns based on long-city class
              if (element.classList.contains('long-city')) {
                element.style.setProperty('grid-template-columns', '1.2fr 1fr 1fr 1.3fr', 'important');
                element.style.setProperty('gap', '0.1cm', 'important');
              } else {
                element.style.setProperty('grid-template-columns', '1.2fr 1fr 1fr 1fr', 'important');
                element.style.setProperty('gap', '0.1cm', 'important');
              }
              
              element.style.setProperty('overflow', 'hidden', 'important');
            });
            
            // Meta items
            const metaItems = document.querySelectorAll('.meta-item');
            metaItems.forEach(function(element) {
              element.style.setProperty('font-family', '"Roboto", Arial, sans-serif', 'important');
              element.style.setProperty('font-size', '6pt', 'important');
              element.style.setProperty('font-weight', '700', 'important');
              element.style.setProperty('line-height', '4.5pt', 'important');
              element.style.setProperty('letter-spacing', '0', 'important');
              element.style.setProperty('word-spacing', '0', 'important');
              element.style.setProperty('padding', '0px 1px', 'important');
              element.style.setProperty('text-rendering', 'optimizeLegibility', 'important');
              element.style.setProperty('-webkit-font-smoothing', 'antialiased', 'important');
              element.style.setProperty('-moz-osx-font-smoothing', 'grayscale', 'important');
            });
            
            // City field (last child) with smaller font for print
            const cityItems = document.querySelectorAll('.meta-item:last-child');
            cityItems.forEach(function(element) {
              if (element.classList.contains('long-city')) {
                element.style.setProperty('font-size', '3pt', 'important');
              } else {
                element.style.setProperty('font-size', '4pt', 'important');
              }
            });
            
            // Meta item data (values) at 6pt
            const metaItemData = document.querySelectorAll('.meta-item b');
            metaItemData.forEach(function(element) {
              element.style.setProperty('font-size', '6pt', 'important');
              element.style.setProperty('font-weight', '600', 'important');
            });
            
            // Apply RajdhaniBold font to all table headers
            const allHeaders = document.querySelectorAll('.main-table th');
            allHeaders.forEach(function(element) {
              element.style.setProperty('font-family', "'RajdhaniBold', Arial, sans-serif", 'important');
              element.style.setProperty('font-weight', 'normal', 'important');
              element.style.setProperty('font-size', '5pt', 'important');
              element.style.setProperty('line-height', '4pt', 'important');
              element.style.setProperty('letter-spacing', '0', 'important');
              element.style.setProperty('font-kerning', 'none', 'important');
              element.style.setProperty('text-rendering', 'optimizeLegibility', 'important');
              element.style.setProperty('-webkit-font-smoothing', 'antialiased', 'important');
              element.style.setProperty('-moz-osx-font-smoothing', 'grayscale', 'important');
            });

            // Colspan 2 headers - increased font size (must run after general header styles)
            const colspan2Headers = document.querySelectorAll('.main-table thead th[colspan="2"]');
            console.log('Found colspan headers:', colspan2Headers.length);
            colspan2Headers.forEach(function(element, index) {
              console.log('Applying styles to colspan header', index, element.textContent);
              element.style.setProperty('font-size', '6pt', 'important');
              element.style.setProperty('font-weight', '1000', 'important');
              console.log('Applied font-size: 6pt, font-weight: 1000 to', element.textContent);
            });

            // Apply Kalimati font specifically to serial number column
            const snHeaders = document.querySelectorAll('.main-table th.col-sn');
            snHeaders.forEach(function(element) {
              element.style.setProperty('font-family', 'Kalimati, Kalimati-Fallback, Noto Sans Devanagari, Hind, Arial, sans-serif', 'important');
              element.style.setProperty('font-weight', '700', 'important'); /* Original font weight for serial number */
              element.style.setProperty('font-size', '5pt', 'important'); /* Original font size for serial number */
              element.style.setProperty('line-height', '4pt', 'important'); /* Original line height for serial number */
            });

            // Apply Kalimati font specifically to position column
            const positionHeaders = document.querySelectorAll('.main-table th.col-position');
            positionHeaders.forEach(function(element) {
              element.style.setProperty('font-family', 'Kalimati, Kalimati-Fallback, Noto Sans Devanagari, Hind, Arial, sans-serif', 'important');
              element.style.setProperty('font-weight', '900', 'important'); /* Increased font weight */
              element.style.setProperty('font-size', '9pt', 'important'); /* Increased by 2pt from 7pt to 9pt */
              element.style.setProperty('line-height', '8pt', 'important'); /* Increased proportionally */
            });

            // Add gap between सि. and नं. in serial number using spans
            const snLine1Elements = document.querySelectorAll('.main-table th.col-sn .sn-line1');
            snLine1Elements.forEach(function(element) {
              element.style.setProperty('display', 'block', 'important');
              element.style.setProperty('margin-bottom', '3pt', 'important'); /* Gap between सि. and नं. */
            });

            const snLine2Elements = document.querySelectorAll('.main-table th.col-sn .sn-line2');
            snLine2Elements.forEach(function(element) {
              element.style.setProperty('display', 'block', 'important');
              element.style.setProperty('margin-top', '0', 'important');
            });

            // Add <br> between numbers and words in hours and days cells
            const hoursCells = document.querySelectorAll('.main-table td.col-hours');
            hoursCells.forEach(function(element) {
              let text = element.innerHTML;
              // Add <br> between number (Arabic or Nepali) and "घण्टा"
              text = text.replace(/([०-९0-9]+)\s*(घण्टा)/g, '$1<br>$2');
              element.innerHTML = text;
                element.style.setProperty('font-size', '6pt', 'important'); /* Reduced font size by 2pt */
              element.style.setProperty('line-height', '9pt', 'important'); /* Increased line height */
            });

            const daysCells = document.querySelectorAll('.main-table td.col-days');
            daysCells.forEach(function(element) {
              let text = element.innerHTML;
              // Add <br> between number (Arabic or Nepali) and "दिन"
              text = text.replace(/([०-९0-9]+)\s*(दिन)/g, '$1<br>$2');
              element.innerHTML = text;
              element.style.setProperty('font-size', '6pt', 'important'); /* Reduced font size by 2pt */
              element.style.setProperty('line-height', '9pt', 'important'); /* Increased line height */
            });

            // Apply reduced font size and spacing to multi-line headers
            const multiLineHeaders = document.querySelectorAll('.main-table th.col-education, .main-table th.col-overtime, .main-table th.col-hours, .main-table th.col-days, .main-table th.col-leave, .main-table th.col-food, .main-table th.col-housing, .main-table th.col-contract');
            multiLineHeaders.forEach(function(element) {
              element.style.setProperty('font-size', '4pt', 'important'); /* Reduced by 1pt from 5pt */
              element.style.setProperty('line-height', '5pt', 'important'); /* Increased for better spacing */
            });

            // Add spacing between line breaks in multi-line headers
            const brElements = document.querySelectorAll('.main-table th.col-education br, .main-table th.col-overtime br, .main-table th.col-hours br, .main-table th.col-days br, .main-table th.col-leave br, .main-table th.col-food br, .main-table th.col-housing br, .main-table th.col-contract br');
            brElements.forEach(function(element) {
              element.style.setProperty('display', 'block', 'important');
              element.style.setProperty('margin', '2.5pt 0', 'important'); /* Increased margin for better spacing */
            });

            // Apply same styling to corresponding table data cells (excluding hours and days)
            const multiLineDataCells = document.querySelectorAll('.main-table td.col-education, .main-table td.col-overtime, .main-table td.col-leave, .main-table td.col-food, .main-table td.col-housing, .main-table td.col-contract');
            multiLineDataCells.forEach(function(element) {
              element.style.setProperty('font-size', '3.5pt', 'important'); /* Reduced by 0.5pt from 4pt */
              element.style.setProperty('line-height', '4.5pt', 'important'); /* Reduced for better spacing */
            });

            // Add spacing between line breaks in data cells
            const dataBrElements = document.querySelectorAll('.main-table td.col-education br, .main-table td.col-overtime br, .main-table td.col-hours br, .main-table td.col-days br, .main-table td.col-leave br, .main-table td.col-food br, .main-table td.col-housing br, .main-table td.col-contract br');
            dataBrElements.forEach(function(element) {
              element.style.setProperty('display', 'block', 'important');
              element.style.setProperty('margin', '2.5pt 0', 'important'); /* Increased margin for better spacing */
            });
            
            // Force line breaks to display in min_qualification field - AGGRESSIVE
            const minQualCells = document.querySelectorAll('.main-table td.col-education, .main-table td.text-center.col-education');
            minQualCells.forEach(function(element) {
              element.style.setProperty('white-space', 'normal', 'important');
              element.style.setProperty('overflow', 'visible', 'important');
              element.style.setProperty('text-overflow', 'initial', 'important');
              element.style.setProperty('line-height', '1.2', 'important');
              element.style.setProperty('word-wrap', 'break-word', 'important');
              element.style.setProperty('overflow-wrap', 'break-word', 'important');
              console.log('Applied line break styles to min_qualification cell:', element.textContent);
              console.log('Cell innerHTML:', element.innerHTML);
              console.log('Cell contains <br>:', element.innerHTML.includes('<br>'));
            });

            // Apply specific width adjustments for salary columns
            const salaryAmountCells = document.querySelectorAll('.main-table td:nth-child(5)'); /* salary_amount - olympia-data */
            salaryAmountCells.forEach(function(element) {
              element.style.setProperty('width', '4%', 'important');
              element.style.setProperty('min-width', '4%', 'important');
              element.style.setProperty('max-width', '4%', 'important');
            });

            const salaryNprCells = document.querySelectorAll('.main-table td:nth-child(6)'); /* salary_npr */
            salaryNprCells.forEach(function(element) {
              element.style.setProperty('width', '8%', 'important');
              element.style.setProperty('min-width', '8%', 'important');
              element.style.setProperty('max-width', '8%', 'important');
            });
            
            // Second row headers - increased font size
            const secondRowHeaders = document.querySelectorAll('.main-table th.col-gender, .main-table th.col-salary');
            secondRowHeaders.forEach(function(element) {
              element.style.setProperty('font-size', '5.3pt', 'important');
              element.style.setProperty('font-weight', '550', 'important');
            });
            
            // Specific data cells - increased font size
            const specificDataCells = document.querySelectorAll('.main-table td:nth-child(3), .main-table td:nth-child(4), .main-table td:nth-child(5), .main-table td:nth-child(6)');
            specificDataCells.forEach(function(element) {
              element.style.setProperty('font-size', '6pt', 'important');
              element.style.setProperty('font-weight', '550', 'important');
            });
            
            // Food and Housing columns - 12.5px font size
            const foodHousingCells = document.querySelectorAll('.col-food-house');
            foodHousingCells.forEach(function(element) {
              element.style.setProperty('font-size', '12.5px', 'important');
              element.style.setProperty('font-weight', '900', 'important');
            });
            
            // Contract Duration column - 8pt font size
            const contractDurationCells = document.querySelectorAll('.col-contract-duration');
            contractDurationCells.forEach(function(element) {
              element.style.setProperty('font-size', '8pt', 'important');
              element.style.setProperty('font-weight', '700', 'important');
            });
            
            // Extra section table - 3.74pt font size
            const extraTableElements = document.querySelectorAll('.extra-table, .extra-table td');
            extraTableElements.forEach(function(element) {
              element.style.setProperty('font-size', '3.04pt', 'important');
              element.style.setProperty('font-weight', '200', 'important');
            });
            
            // Apply line-height to td elements
            const extraTableTds = document.querySelectorAll('.extra-table td');
            extraTableTds.forEach(function(element) {
              element.style.setProperty('line-height', '1.2', 'important');
            });
            
            // Apply increased line-height to td elements with br tags
            const extraTableTdsWithBr = document.querySelectorAll('.extra-table td');
            extraTableTdsWithBr.forEach(function(element) {
              if (element.innerHTML.includes('<br')) {
                element.style.setProperty('line-height', '1.4', 'important');
              }
            });
            
            // Apply special styling to col-service-fee cells
            const serviceFeeCells = document.querySelectorAll('.extra-table td.col-service-fee');
            serviceFeeCells.forEach(function(element) {
              element.style.setProperty('font-size', '5.54pt', 'important'); /* Reduced by 0.5pt from 6.04pt */
              element.style.setProperty('font-weight', '700', 'important');
            });
            
            // Apply special styling to currency amounts
            const currencyAmountSpans = document.querySelectorAll('.extra-table .currency-amount');
            currencyAmountSpans.forEach(function(element) {
              element.style.setProperty('font-size', '3pt', 'important'); /* Reduced by 2pt from 7pt */
              element.style.setProperty('font-weight', '700', 'important');
            });
            
            // Extra table headers with specific styling
            const extraTableHeaders = document.querySelectorAll('.extra-table th');
            extraTableHeaders.forEach(function(element) {
              element.style.setProperty('font-size', '3pt', 'important');
              element.style.setProperty('font-weight', '500', 'important');
              element.style.setProperty('line-height', '4pt', 'important');
              element.style.setProperty('letter-spacing', '0', 'important');
              element.style.setProperty('font-kerning', 'auto', 'important');
            });
            
            // Mark as processed to prevent re-execution
            fontsProcessed = true;
          }
          
          // Production-ready event listeners - no flickering
          window.addEventListener('beforeprint', forceLightFontWeights);
          window.addEventListener('print', forceLightFontWeights);
          
          // Run once on page load - no timeouts to prevent flickering
          document.addEventListener('DOMContentLoaded', function() {
            // Run immediately - no delays
            forceLightFontWeights();
          });
          
          // Nepali calendar conversion function
          function gregorianToNepali(gregorianDate) {
            // Base date: 1943-04-14 (Gregorian) = 2000-01-01 (Nepali)
            const baseDate = new Date(1943, 3, 14); // Month is 0-indexed
            const baseNepaliYear = 2000;
            const baseNepaliMonth = 1;
            const baseNepaliDay = 1;
            
            // Calculate days difference
            const timeDiff = gregorianDate.getTime() - baseDate.getTime();
            const daysDiff = Math.floor(timeDiff / (1000 * 3600 * 24));
            
            // Nepali calendar data (days in each month for years 2000-2090)
            const nepaliCalendar = {
              2000: [30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 30],
              2001: [31, 31, 32, 31, 31, 29, 30, 30, 29, 30, 29, 31],
              2002: [31, 31, 32, 31, 31, 29, 30, 30, 29, 30, 29, 31],
              2003: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
              2004: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 30],
              2005: [31, 31, 32, 32, 31, 30, 30, 30, 29, 30, 29, 31],
              2006: [30, 31, 32, 32, 31, 30, 30, 30, 29, 30, 29, 30],
              2007: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
              2008: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 30],
              2009: [31, 31, 32, 32, 31, 31, 30, 30, 29, 30, 29, 31],
              2010: [30, 31, 32, 32, 31, 30, 30, 30, 29, 30, 29, 30],
              2011: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
              2012: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 30],
              2013: [31, 31, 32, 32, 31, 30, 30, 30, 29, 30, 29, 31],
              2014: [30, 31, 32, 32, 31, 30, 30, 30, 29, 30, 29, 30],
              2015: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
              2016: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 30],
              2017: [31, 31, 32, 32, 31, 31, 30, 30, 29, 30, 29, 31],
              2018: [30, 31, 32, 32, 31, 30, 30, 30, 29, 30, 29, 30],
              2019: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
              2020: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 30],
              2021: [31, 31, 32, 32, 31, 30, 30, 30, 29, 30, 29, 31],
              2022: [30, 31, 32, 32, 31, 30, 30, 30, 29, 30, 29, 30],
              2023: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
              2024: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 30],
              2025: [31, 31, 32, 32, 31, 31, 30, 30, 29, 30, 29, 31],
              2026: [30, 31, 32, 32, 31, 30, 30, 30, 29, 30, 29, 30],
              2027: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
              2028: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 30],
              2029: [31, 31, 32, 32, 31, 30, 30, 30, 29, 30, 29, 31],
              2030: [30, 31, 32, 32, 31, 30, 30, 30, 29, 30, 29, 30],
              2031: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
              2032: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 30],
              2033: [31, 31, 32, 32, 31, 31, 30, 30, 29, 30, 29, 31],
              2034: [30, 31, 32, 32, 31, 30, 30, 30, 29, 30, 29, 30],
              2035: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
              2036: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 30],
              2037: [31, 31, 32, 32, 31, 30, 30, 30, 29, 30, 29, 31],
              2038: [30, 31, 32, 32, 31, 30, 30, 30, 29, 30, 29, 30],
              2039: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
              2040: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 30],
              2041: [31, 31, 32, 32, 31, 31, 30, 30, 29, 30, 29, 31],
              2042: [30, 31, 32, 32, 31, 30, 30, 30, 29, 30, 29, 30],
              2043: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
              2044: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 30],
              2045: [31, 31, 32, 32, 31, 30, 30, 30, 29, 30, 29, 31],
              2046: [30, 31, 32, 32, 31, 30, 30, 30, 29, 30, 29, 30],
              2047: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
              2048: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 30],
              2049: [31, 31, 32, 32, 31, 31, 30, 30, 29, 30, 29, 31],
              2050: [30, 31, 32, 32, 31, 30, 30, 30, 29, 30, 29, 30],
              2051: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
              2052: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 30],
              2053: [31, 31, 32, 32, 31, 30, 30, 30, 29, 30, 29, 31],
              2054: [30, 31, 32, 32, 31, 30, 30, 30, 29, 30, 29, 30],
              2055: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
              2056: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 30],
              2057: [31, 31, 32, 32, 31, 31, 30, 30, 29, 30, 29, 31],
              2058: [30, 31, 32, 32, 31, 30, 30, 30, 29, 30, 29, 30],
              2059: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
              2060: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 30],
              2061: [31, 31, 32, 32, 31, 30, 30, 30, 29, 30, 29, 31],
              2062: [30, 31, 32, 32, 31, 30, 30, 30, 29, 30, 29, 30],
              2063: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
              2064: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 30],
              2065: [31, 31, 32, 32, 31, 31, 30, 30, 29, 30, 29, 31],
              2066: [30, 31, 32, 32, 31, 30, 30, 30, 29, 30, 29, 30],
              2067: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
              2068: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 30],
              2069: [31, 31, 32, 32, 31, 30, 30, 30, 29, 30, 29, 31],
              2070: [30, 31, 32, 32, 31, 30, 30, 30, 29, 30, 29, 30],
              2071: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
              2072: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 30],
              2073: [31, 31, 32, 32, 31, 31, 30, 30, 29, 30, 29, 31],
              2074: [30, 31, 32, 32, 31, 30, 30, 30, 29, 30, 29, 30],
              2075: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
              2076: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 30],
              2077: [31, 31, 32, 32, 31, 30, 30, 30, 29, 30, 29, 31],
              2078: [30, 31, 32, 32, 31, 30, 30, 30, 29, 30, 29, 30],
              2079: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
              2080: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 30],
              2081: [31, 31, 32, 32, 31, 31, 30, 30, 29, 30, 29, 31],
              2082: [30, 31, 32, 32, 31, 30, 30, 30, 29, 30, 29, 30],
              2083: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
              2084: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 30],
              2085: [31, 31, 32, 32, 31, 30, 30, 30, 29, 30, 29, 31],
              2086: [30, 31, 32, 32, 31, 30, 30, 30, 29, 30, 29, 30],
              2087: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
              2088: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 30],
              2089: [31, 31, 32, 32, 31, 31, 30, 30, 29, 30, 29, 31],
              2090: [30, 31, 32, 32, 31, 30, 30, 30, 29, 30, 29, 30]
            };
            
            // Convert days to Nepali date
            let remainingDays = daysDiff;
            let nepaliYear = baseNepaliYear;
            let nepaliMonth = baseNepaliMonth;
            let nepaliDay = baseNepaliDay;
            
            // Find the year
            while (remainingDays > 0 && nepaliYear <= 2090) {
              const yearDays = nepaliCalendar[nepaliYear].reduce((sum, days) => sum + days, 0);
              if (remainingDays >= yearDays) {
                remainingDays -= yearDays;
                nepaliYear++;
              } else {
                break;
              }
            }
            
            // Find the month
            while (remainingDays > 0 && nepaliMonth <= 12) {
              const monthDays = nepaliCalendar[nepaliYear][nepaliMonth - 1];
              if (remainingDays >= monthDays) {
                remainingDays -= monthDays;
                nepaliMonth++;
              } else {
                break;
              }
            }
            
            // Calculate the day
            nepaliDay = remainingDays + 1;
            
            // Convert to Nepali numerals
            const nepaliNumerals = ['०', '१', '२', '३', '४', '५', '६', '७', '८', '९'];
            const nepaliMonths = ['', 'बैशाख', 'जेठ', 'असार', 'श्रावण', 'भदौ', 'असोज', 'कार्तिक', 'मंसिर', 'पुष', 'माघ', 'फाल्गुन', 'चैत'];
            
            function toNepaliNumeral(num) {
              return num.toString().split('').map(digit => nepaliNumerals[parseInt(digit)]).join('');
            }
            
            return {
              year: toNepaliNumeral(nepaliYear),
              month: toNepaliNumeral(nepaliMonth.toString().padStart(2, '0')),
              day: toNepaliNumeral(nepaliDay.toString().padStart(2, '0')),
              monthName: nepaliMonths[nepaliMonth]
            };
          }
          
          // Function to calculate interview date (8 days after pre-approval)
          function calculateInterviewDate() {
            const preApprovalDate = '{{ ad.pre_approval_date }}';
            const calculatedNepaliDate = document.getElementById('calculated-interview-date');
            const calculatedEnglishDate = document.getElementById('calculated-interview-date-english');
            
            if (!calculatedNepaliDate || !calculatedEnglishDate) {
              // Elements don't exist, nothing to update
              return;
            }
            
            if (preApprovalDate && preApprovalDate !== 'None' && preApprovalDate !== '') {
              try {
                const date = new Date(preApprovalDate);
                if (!isNaN(date.getTime())) {
                  date.setDate(date.getDate() + 8);
                  
                  // Format English date as "30 August, 2025"
                  const englishOptions = { year: 'numeric', month: 'long', day: 'numeric' };
                  const englishDate = date.toLocaleDateString('en-US', englishOptions);
                  
                  // Convert to Nepali date
                  const nepaliDate = gregorianToNepali(date);
                  const nepaliDateString = `${nepaliDate.year}/${nepaliDate.month}/${nepaliDate.day}`;
                  
                  calculatedNepaliDate.textContent = nepaliDateString;
                  calculatedEnglishDate.textContent = englishDate;
                } else {
                  calculatedNepaliDate.textContent = 'निर्धारण गर्नुहोस्';
                  calculatedEnglishDate.textContent = 'निर्धारण गर्नुहोस्';
                }
              } catch (e) {
                console.error('Error calculating interview date:', e);
                calculatedNepaliDate.textContent = 'निर्धारण गर्नुहोस्';
                calculatedEnglishDate.textContent = 'निर्धारण गर्नुहोस्';
              }
            } else {
              calculatedNepaliDate.textContent = 'निर्धारण गर्नुहोस्';
              calculatedEnglishDate.textContent = 'निर्धारण गर्नुहोस्';
            }
          }
          
          // Calculate interview date when DOM is ready
          document.addEventListener('DOMContentLoaded', function() {
            calculateInterviewDate();
          });
          
          // Also run immediately if DOM is already loaded
          if (document.readyState === 'loading') {
            // DOM is still loading, DOMContentLoaded will handle it
          } else {
            // DOM is already loaded, run immediately
            calculateInterviewDate();
          }
        


// NUCLEAR APPROACH - Force colspan header styles with multiple attempts
function forceColspanStyles() {
  console.log('NUCLEAR - Starting colspan style enforcement');
  
  // Try multiple selectors
  const selectors = [
    '.main-table thead tr th[colspan="2"]',
    'th[colspan="2"]',
    '#main-table thead tr th[colspan="2"]',
    'table th[colspan="2"]'
  ];
  
  selectors.forEach(function(selector, index) {
    const elements = document.querySelectorAll(selector);
    console.log('NUCLEAR - Selector', index, selector, 'found', elements.length, 'elements');
    
    elements.forEach(function(element, elemIndex) {
      console.log('NUCLEAR - Applying to element', elemIndex, element.textContent);
      
      // Multiple approaches to force the styles
      element.style.setProperty('font-size', '6.3pt', 'important');
      element.style.setProperty('font-weight', '900', 'important');
      element.style.setProperty('font-family', 'Arial, sans-serif', 'important');
      
      element.style.fontSize = '6.3pt';
      element.style.fontWeight = '900';
      element.style.fontFamily = 'Arial, sans-serif';
      
      // Set attributes directly
      const currentStyle = element.getAttribute('style') || '';
      element.setAttribute('style', currentStyle + '; font-size: 6.3pt !important; font-weight: 900 !important; font-family: Arial, sans-serif !important;');
      
      // Force with CSS class
      element.classList.add('force-colspan-style');
      
      console.log('NUCLEAR - Applied styles to', element.textContent);
      console.log('NUCLEAR - Element style:', element.getAttribute('style'));
    });
  });
}

// Run immediately
document.addEventListener('DOMContentLoaded', function() {
  forceColspanStyles();
  
  // Run again after 500ms
  setTimeout(forceColspanStyles, 500);
  
  // Run again after 1000ms
  setTimeout(forceColspanStyles, 1000);
  
  // Run again after 2000ms
  setTimeout(forceColspanStyles, 2000);
});

// Also run on window load
window.addEventListener('load', function() {
  forceColspanStyles();
});
