from nicegui import ui
from app.counter_service import CounterService


def create():
    """Create the counter application UI."""

    @ui.page("/counter")
    async def counter_page():
        """Counter application page with modern styling."""

        # Apply modern theme colors
        ui.colors(
            primary="#2563eb",
            secondary="#64748b",
            accent="#10b981",
            positive="#10b981",
            negative="#ef4444",
            warning="#f59e0b",
            info="#3b82f6",
        )

        # Page title
        ui.label("Counter Application").classes("text-3xl font-bold text-gray-800 mb-8 text-center")

        # Get initial counter value
        current_value = CounterService.get_counter_value()

        # Main container with modern card design
        with ui.card().classes("w-96 mx-auto p-8 shadow-xl rounded-2xl bg-white"):
            # Counter display with large, prominent styling
            with ui.row().classes("justify-center mb-8"):
                counter_display = (
                    ui.label(str(current_value))
                    .classes(
                        "text-6xl font-bold text-primary bg-gray-50 px-6 py-4 rounded-xl border-2 border-gray-200 min-w-32 text-center"
                    )
                    .mark("counter-display")
                )

            # Button container with proper spacing
            with ui.row().classes("gap-4 justify-center mb-6"):
                # Decrement button with modern styling
                ui.button("−", on_click=lambda: handle_decrement()).classes(
                    "text-3xl font-bold px-6 py-3 bg-red-500 hover:bg-red-600 text-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-200"
                ).mark("decrement-btn")

                # Increment button with modern styling
                ui.button("+", on_click=lambda: handle_increment()).classes(
                    "text-3xl font-bold px-6 py-3 bg-green-500 hover:bg-green-600 text-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-200"
                ).mark("increment-btn")

            # Reset button with subtle styling
            ui.button("Reset", on_click=lambda: handle_reset()).classes(
                "w-full py-3 bg-gray-500 hover:bg-gray-600 text-white rounded-xl shadow-md hover:shadow-lg transition-all duration-200"
            ).mark("reset-btn")

            # Current value info
            ui.label("Click + to increment, − to decrement, or Reset to start over").classes(
                "text-sm text-gray-500 text-center mt-4"
            )

        def handle_increment():
            """Handle increment button click."""
            try:
                new_value = CounterService.increment_counter()
                counter_display.set_text(str(new_value))
                ui.notify(f"Counter incremented to {new_value}", type="positive")
            except Exception as e:
                import logging

                logging.exception("Error incrementing counter")
                ui.notify(f"Error incrementing counter: {str(e)}", type="negative")

        def handle_decrement():
            """Handle decrement button click."""
            try:
                new_value = CounterService.decrement_counter()
                counter_display.set_text(str(new_value))
                ui.notify(f"Counter decremented to {new_value}", type="info")
            except Exception as e:
                import logging

                logging.exception("Error decrementing counter")
                ui.notify(f"Error decrementing counter: {str(e)}", type="negative")

        def handle_reset():
            """Handle reset button click."""
            try:
                new_value = CounterService.reset_counter()
                counter_display.set_text(str(new_value))
                ui.notify("Counter reset to 0", type="warning")
            except Exception as e:
                import logging

                logging.exception("Error resetting counter")
                ui.notify(f"Error resetting counter: {str(e)}", type="negative")

    @ui.page("/")
    def index():
        """Home page with navigation to counter."""
        ui.colors(primary="#2563eb", secondary="#64748b", accent="#10b981")

        with ui.column().classes("items-center justify-center min-h-screen bg-gray-50 p-8"):
            ui.label("Welcome to the Counter App").classes("text-4xl font-bold text-gray-800 mb-4")
            ui.label("A simple counter application with increment, decrement, and reset functionality.").classes(
                "text-lg text-gray-600 mb-8 max-w-2xl text-center"
            )

            ui.button("Open Counter", on_click=lambda: ui.navigate.to("/counter")).classes(
                "px-8 py-4 bg-primary hover:bg-blue-700 text-white text-lg font-semibold rounded-xl shadow-lg hover:shadow-xl transition-all duration-200"
            )
