# services.py

class ConversionService:
    """Handles all tile size and box to square meter/feet conversions."""

    # Tile packing configurations (boxes to tiles, and then tiles to SQM)
    PACKING_CONFIGS = {
        "600x600": {"tiles_per_box": 4, "tile_size_sqm": 0.36}, # Assuming 4 tiles for 1.44 SQM
        "600x1200_2_tile": {"tiles_per_box": 2, "tile_size_sqm": 0.72}, # For 1.44 SQM per box
        "600x1200_3_tile": {"tiles_per_box": 3, "tile_size_sqm": 0.72}, # For 2.16 SQM per box
        "800x1600": {"tiles_per_box": 2, "tile_size_sqm": 1.28}, # Assuming 2 tiles for 2.56 SQM
        "1200x1800": {"tiles_per_box": 2, "tile_size_sqm": 2.16}, # Assuming 2 tiles for 4.32 SQM
    }

    # Define the final SQM per box for simplicity based on your requirements
    BOX_SQM_MAP = {
        "600x600": 1.44,
        "600x1200_standard": 1.44, # For Premium, Standard, Commercial
        "600x1200_eco_rej": 2.16,   # For Eco, Rejection
        "800x1600": 2.56,
        "1200x1800": 4.32,
    }

    SQM_TO_SQFT_FACTOR = 10.764

    @staticmethod
    def get_tile_type_key(size, quality):
        """Helper to get the correct key for BOX_SQM_MAP."""
        if size == "600x1200":
            if quality in ["ECO", "REJ"]:
                return "600x1200_eco_rej"
            else:
                return "600x1200_standard"
        return size # For other sizes, size itself is the key

    @staticmethod
    def convert_boxes_to_sqm(size, quality, boxes):
        """Converts number of boxes to square meters."""
        tile_type_key = ConversionService.get_tile_type_key(size, quality)
        sqm_per_box = ConversionService.BOX_SQM_MAP.get(tile_type_key)
        if sqm_per_box is None:
            raise ValueError(f"Invalid tile size or quality combination: {size}, {quality}")
        return round(boxes * sqm_per_box, 2) # Round to 2 decimal places

    @staticmethod
    def convert_sqm_to_sqft(sqm):
        """Converts square meters to square feet."""
        return round(sqm * ConversionService.SQM_TO_SQFT_FACTOR, 2)

class StockService:
    """Manages the in-memory stock."""
    # This is a very simple in-memory stock.
    # In a real application, this would interact with a database.
    _stock = {} # Format: { 'tile_key': { 'boxes': N, 'sqm': M, 'sqft': P } }

    @staticmethod
    def get_stock_key(size, thickness, quality, plant_code):
        return f"{size}_{thickness}mm_{quality}_{plant_code}"

    @staticmethod
    def add_production(size, thickness, quality, plant_code, boxes):
        key = StockService.get_stock_key(size, thickness, quality, plant_code)
        
        sqm_produced = ConversionService.convert_boxes_to_sqm(size, quality, boxes)
        sqft_produced = ConversionService.convert_sqm_to_sqft(sqm_produced)

        if key not in StockService._stock:
            StockService._stock[key] = {'boxes': 0, 'sqm': 0.0, 'sqft': 0.0}

        StockService._stock[key]['boxes'] += boxes
        StockService._stock[key]['sqm'] += sqm_produced
        StockService._stock[key]['sqft'] += sqft_produced
        
        return StockService._stock[key]

    @staticmethod
    def get_all_stock():
        return StockService._stock

    @staticmethod
    def reset_stock(): # For demonstration/testing
        StockService._stock = {}
