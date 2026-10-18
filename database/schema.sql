PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS properties (
    property_id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_name TEXT NOT NULL,
    address TEXT NOT NULL,
    city TEXT NOT NULL,
    property_type TEXT DEFAULT 'Residential'
);

CREATE TABLE IF NOT EXISTS rooms (
    room_id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_id INTEGER NOT NULL,
    room_number TEXT NOT NULL,
    monthly_rent REAL NOT NULL CHECK(monthly_rent >= 0),
    status TEXT NOT NULL CHECK(status IN ('occupied', 'vacant')),

    FOREIGN KEY (property_id)
        REFERENCES properties(property_id),

    UNIQUE(property_id, room_number)
);

CREATE TABLE IF NOT EXISTS tenants (
    tenant_id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_id INTEGER NOT NULL UNIQUE,
    tenant_name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    lease_start DATE,
    lease_end DATE,

    FOREIGN KEY (room_id)
        REFERENCES rooms(room_id)
);

CREATE TABLE IF NOT EXISTS payments (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    tenant_id INTEGER NOT NULL,
    rent_month TEXT NOT NULL,
    amount_due REAL NOT NULL CHECK(amount_due >= 0),
    amount_paid REAL NOT NULL DEFAULT 0
        CHECK(amount_paid >= 0),
    due_date DATE NOT NULL,
    payment_date DATE,
    status TEXT NOT NULL
        CHECK(status IN ('paid', 'partial', 'pending', 'overdue')),

    FOREIGN KEY (tenant_id)
        REFERENCES tenants(tenant_id),

    UNIQUE(tenant_id, rent_month)
);

CREATE INDEX IF NOT EXISTS idx_payments_tenant
ON payments(tenant_id);

CREATE INDEX IF NOT EXISTS idx_payments_due_date
ON payments(due_date);

CREATE INDEX IF NOT EXISTS idx_rooms_property
ON rooms(property_id);