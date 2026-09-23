/* ==========================================================================
   Digital Darts - Admin Dashboard JavaScript (CRM, Blog & Settings Handlers)
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Audit Lead CRM Filters & Status Toggles
  const statusFilter = document.getElementById('adminStatusFilter');
  const adminSearch = document.getElementById('adminSearchInput');
  const leadRows = document.querySelectorAll('.lead-table-row');
  const visibleLeadCountText = document.getElementById('visibleLeadCount');
  let currentActiveRow = null;

  const updateVisibleCount = () => {
    let count = 0;
    leadRows.forEach(row => {
      if (row.style.display !== 'none') count++;
    });
    if (visibleLeadCountText) {
      visibleLeadCountText.innerText = count + ' Inquiry' + (count === 1 ? '' : 'ies');
    }
  };

  if (statusFilter) {
    statusFilter.addEventListener('change', (e) => {
      const selectedStatus = e.target.value;
      leadRows.forEach(row => {
        const rowStatus = row.getAttribute('data-status');
        if (selectedStatus === 'all' || rowStatus === selectedStatus) {
          row.style.display = '';
        } else {
          row.style.display = 'none';
        }
      });
      updateVisibleCount();
    });
  }

  if (adminSearch) {
    adminSearch.addEventListener('keyup', (e) => {
      const query = e.target.value.toLowerCase();
      leadRows.forEach(row => {
        const text = row.innerText.toLowerCase();
        if (text.includes(query)) {
          row.style.display = '';
        } else {
          row.style.display = 'none';
        }
      });
      updateVisibleCount();
    });
  }

  // Lead Details Modal Inspection Handler
  const leadModalEl = document.getElementById('leadDetailModal');
  if (leadModalEl) {
    const inspectButtons = document.querySelectorAll('.btn-inspect-lead');
    const modalStoreName = document.getElementById('modalStoreName');
    const modalStoreUrl = document.getElementById('modalStoreUrl');
    const modalStatusBadge = document.getElementById('modalStatusBadge');
    const modalContactName = document.getElementById('modalContactName');
    const modalContactEmail = document.getElementById('modalContactEmail');
    const modalRevenue = document.getElementById('modalRevenue');
    const modalAdSpend = document.getElementById('modalAdSpend');
    const modalGoalNotes = document.getElementById('modalGoalNotes');

    inspectButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        const rowId = btn.getAttribute('data-id');
        currentActiveRow = document.querySelector(`.lead-table-row[data-id="${rowId}"]`);

        const name = btn.getAttribute('data-name');
        const store = btn.getAttribute('data-store');
        const url = btn.getAttribute('data-url');
        const email = btn.getAttribute('data-email');
        const rev = btn.getAttribute('data-rev');
        const spend = btn.getAttribute('data-spend');
        const goal = btn.getAttribute('data-goal');
        const status = btn.getAttribute('data-status');

        if (modalStoreName) modalStoreName.innerText = store;
        if (modalStoreUrl) {
          modalStoreUrl.innerText = url;
          modalStoreUrl.href = url;
        }
        if (modalContactName) modalContactName.innerText = name;
        if (modalContactEmail) modalContactEmail.innerText = email;
        if (modalRevenue) modalRevenue.innerText = rev;
        if (modalAdSpend) modalAdSpend.innerText = spend;
        if (modalGoalNotes) modalGoalNotes.innerText = goal;

        if (modalStatusBadge) {
          modalStatusBadge.className = 'badge-status ' + status;
          let labelText = 'New Request';
          if (status === 'audit_sent') labelText = 'Audit Sent';
          if (status === 'closed_won') labelText = 'Closed Won';
          if (status === 'closed_lost') labelText = 'Closed Lost';
          modalStatusBadge.innerText = labelText;
        }

        const bsModal = new bootstrap.Modal(leadModalEl);
        bsModal.show();
      });
    });

    const updateButtons = document.querySelectorAll('.btn-update-status');
    updateButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        const newStatus = btn.getAttribute('data-status');
        if (currentActiveRow) {
          currentActiveRow.setAttribute('data-status', newStatus);
          const badgeEl = currentActiveRow.querySelector('.badge-status');
          if (badgeEl) {
            badgeEl.className = 'badge-status ' + newStatus;
            let iconHtml = '<i class="fas fa-circle" style="font-size: 0.5rem;"></i> New Request';
            if (newStatus === 'audit_sent') iconHtml = '<i class="fas fa-paper-plane" style="font-size: 0.6rem;"></i> Audit Sent';
            if (newStatus === 'closed_won') iconHtml = '<i class="fas fa-check" style="font-size: 0.6rem;"></i> Closed Won';
            if (newStatus === 'closed_lost') iconHtml = '<i class="fas fa-times" style="font-size: 0.6rem;"></i> Closed Lost';
            badgeEl.innerHTML = iconHtml;
          }

          if (modalStatusBadge) {
            modalStatusBadge.className = 'badge-status ' + newStatus;
            let labelText = 'New Request';
            if (newStatus === 'audit_sent') labelText = 'Audit Sent';
            if (newStatus === 'closed_won') labelText = 'Closed Won';
            if (newStatus === 'closed_lost') labelText = 'Closed Lost';
            modalStatusBadge.innerText = labelText;
          }
        }
      });
    });
  }

  // 2. Blog Post Manager Real-Time Handlers
  const blogStatusFilter = document.getElementById('blogStatusFilter');
  const blogSearchInput = document.getElementById('blogSearchInput');
  const blogGrid = document.getElementById('adminBlogGrid');

  if (blogStatusFilter && blogGrid) {
    blogStatusFilter.addEventListener('change', (e) => {
      const val = e.target.value;
      const items = blogGrid.querySelectorAll('.blog-admin-item');
      items.forEach(item => {
        const st = item.getAttribute('data-status');
        if (val === 'all' || st === val) {
          item.style.display = '';
        } else {
          item.style.display = 'none';
        }
      });
    });
  }

  if (blogSearchInput && blogGrid) {
    blogSearchInput.addEventListener('keyup', (e) => {
      const q = e.target.value.toLowerCase();
      const items = blogGrid.querySelectorAll('.blog-admin-item');
      items.forEach(item => {
        const text = item.innerText.toLowerCase();
        if (text.includes(q)) {
          item.style.display = '';
        } else {
          item.style.display = 'none';
        }
      });
    });
  }

  // Blog Publish / Unpublish Toggle
  document.addEventListener('click', (e) => {
    const toggleBtn = e.target.closest('.btn-toggle-publish');
    if (toggleBtn) {
      const card = toggleBtn.closest('.blog-admin-item');
      const isPublished = toggleBtn.getAttribute('data-published') === 'true';
      const statusBadge = card.querySelector('.badge.bg-success, .badge.bg-warning');

      if (isPublished) {
        toggleBtn.setAttribute('data-published', 'false');
        toggleBtn.className = 'btn btn-sm btn-success btn-toggle-publish';
        toggleBtn.innerHTML = '<i class="fas fa-paper-plane me-1"></i> Publish';
        card.setAttribute('data-status', 'draft');
        if (statusBadge) {
          statusBadge.className = 'badge bg-warning text-dark';
          statusBadge.innerText = 'Draft';
        }
      } else {
        toggleBtn.setAttribute('data-published', 'true');
        toggleBtn.className = 'btn btn-sm btn-outline-dark btn-toggle-publish';
        toggleBtn.innerHTML = '<i class="fas fa-eye-slash me-1"></i> Unpublish';
        card.setAttribute('data-status', 'published');
        if (statusBadge) {
          statusBadge.className = 'badge bg-success text-white';
          statusBadge.innerText = 'Published';
        }
      }
    }

    const deleteBtn = e.target.closest('.btn-delete-post');
    if (deleteBtn) {
      const card = deleteBtn.closest('.blog-admin-item');
      if (card) {
        card.remove();
      }
    }
  });

  // Create New Article Form Handler
  const createPostForm = document.getElementById('createPostForm');
  if (createPostForm && blogGrid) {
    createPostForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const title = document.getElementById('postTitleInput').value;
      const category = document.getElementById('postCategoryInput').value;
      const readTime = document.getElementById('postReadTimeInput').value;
      const excerpt = document.getElementById('postExcerptInput').value;

      const newCardHtml = `
        <div class="col-md-6 col-lg-4 blog-admin-item" data-status="published">
          <div class="blog-admin-card h-100 d-flex flex-column">
            <img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=800&q=80" class="blog-admin-card-img" alt="${title}">
            <div class="p-4 d-flex flex-column flex-grow-1">
              <div class="d-flex justify-content-between align-items-center mb-2">
                <span class="badge bg-sage text-dark fw-bold">${category}</span>
                <span class="badge bg-success text-white">Published</span>
              </div>
              <h5 class="fw-bold text-dark mb-2">${title}</h5>
              <p class="small text-muted mb-4">${excerpt}</p>
              
              <div class="mt-auto pt-3 border-top d-flex justify-content-between align-items-center">
                <span class="small text-muted"><i class="far fa-clock me-1"></i> ${readTime} Min Read</span>
                <div class="d-flex gap-1">
                  <button class="btn btn-sm btn-outline-dark btn-toggle-publish" data-published="true"><i class="fas fa-eye-slash"></i> Unpublish</button>
                  <button class="btn btn-sm btn-outline-danger btn-delete-post"><i class="fas fa-trash"></i></button>
                </div>
              </div>
            </div>
          </div>
        </div>
      `;

      blogGrid.insertAdjacentHTML('afterbegin', newCardHtml);
      createPostForm.reset();

      const modalEl = document.getElementById('newPostModal');
      const bsModal = bootstrap.Modal.getInstance(modalEl);
      if (bsModal) bsModal.hide();
    });
  }

  // 3. Settings Save Notification Handler
  const settingsAlert = document.getElementById('settingsAlert');
  const agencyProfileForm = document.getElementById('agencyProfileForm');
  const roiConfigForm = document.getElementById('roiConfigForm');

  const showSettingsSaveAlert = () => {
    if (settingsAlert) {
      settingsAlert.classList.remove('d-none');
      window.scrollTo({ top: 0, behavior: 'smooth' });
      setTimeout(() => {
        settingsAlert.classList.add('d-none');
      }, 3500);
    }
  };

  if (agencyProfileForm) {
    agencyProfileForm.addEventListener('submit', (e) => {
      e.preventDefault();
      showSettingsSaveAlert();
    });
  }

  if (roiConfigForm) {
    roiConfigForm.addEventListener('submit', (e) => {
      e.preventDefault();
      showSettingsSaveAlert();
    });
  }
});
