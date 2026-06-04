# Menu Management System

## Models

### Category
- `name` (CharField, max 120 chars)
- `description` (TextField, optional)

### MenuItem
- `category` (ForeignKey to Category)
- `name` (CharField, max 140 chars)
- `description` (TextField, optional)
- `price` (DecimalField, up to 8 digits, 2 decimal places)
- `is_available` (BooleanField, default True)
- `preparation_time` (PositiveIntegerField, in minutes, default 15)
- `image` (ImageField, upload to `menu_items/`, optional)
- `customizations` (JSONField, for storing item variants/options, default empty dict)

## Admin Panel Features

### Category Admin
- List view displays category name and item count
- Ordered by name alphabetically
- Editable from list view

### MenuItem Admin
- List display: name, category, price, is_available, preparation_time
- List filters: category, is_available
- Inline editing: is_available and price fields
- Search: by name and description
- Organized fieldsets:
  - Basic Info (name, category, description, image)
  - Pricing & Availability (price, is_available, preparation_time)
  - Customizations (collapsible section for advanced options)

## Frontend Features

### Menu Display (/menu/)
- Items displayed in a responsive grid layout
- Shows item image (or placeholder if missing)
- Displays item name, description, price, and preparation time
- Availability status badge (green for available, red for unavailable)
- Organized by category

### Image Uploads
- Images stored in `media/menu_items/` directory
- Configured in Django settings with `MEDIA_URL` and `MEDIA_ROOT`
- Media files served in development via Django

## Usage

### Adding a Menu Item
1. Go to `/admin/`
2. Navigate to "Menu Items"
3. Click "Add Menu Item"
4. Fill in details:
   - Select a category
   - Enter name and description
   - Set price and preparation time
   - Upload an optional image
   - Add customizations as JSON (e.g., `{"spice": ["mild", "hot"]}`)
5. Save

### Marking Items Unavailable
1. From the Menu Items list view
2. Uncheck the "is_available" checkbox directly in the list
3. Click Save

## JSON Customizations Example
```json
{
  "spice_level": ["mild", "medium", "hot"],
  "size": ["small", "large"],
  "extra_cheese": true
}
```

This structure can be extended to include order-time customizations in future features.
