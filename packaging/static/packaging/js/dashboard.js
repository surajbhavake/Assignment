
const form = document.getElementById("recommendation-form");
const orderInput = document.getElementById("order-id");
const button = document.getElementById("recommend-button");
const feedback = document.getElementById("feedback");
const resultPanel = document.getElementById("result-panel");

function showFeedback(message, isError = false) {
    feedback.textContent = message;
    feedback.classList.toggle("error", isError);
}

function formatMoney(value) {
    return new Intl.NumberFormat("en-IN", {
        style: "currency",
        currency: "INR",
    }).format(Number(value));
}

function displayResult(data) {
    const box = data.recommended_box;

    document.getElementById("selected-order").textContent =
        data.order_number;

    document.getElementById("total-weight").textContent =
        `${data.total_weight_kg} kg`;

    document.getElementById("box-cost").textContent =
        formatMoney(box.cost);

    document.getElementById("recommended-box").textContent =
        box.name;

    document.getElementById("box-dimensions").textContent =
        `${box.dimensions_cm.length} × ` +
        `${box.dimensions_cm.width} × ` +
        `${box.dimensions_cm.height} cm`;

    document.getElementById("max-weight").textContent =
        `${box.maximum_weight_kg} kg`;

    document.getElementById("result-weight").textContent =
        `${data.total_weight_kg} kg`;

    document.getElementById("result-cost").textContent =
        formatMoney(box.cost);

    resultPanel.hidden = false;
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const orderId = orderInput.value.trim();

    if (!orderId || Number(orderId) < 1) {
        showFeedback("Please enter a valid order ID.", true);
        return;
    }

    button.disabled = true;
    button.textContent = "Checking boxes...";
    resultPanel.hidden = true;
    showFeedback("Calculating the best available box...");

    try {
        const response = await fetch(
            `/api/orders/${encodeURIComponent(orderId)}/recommend-box/`,
            {
                headers: {
                    Accept: "application/json",
                },
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.error || data.message ||
                "Unable to recommend a box for this order."
            );
        }

        displayResult(data);
        showFeedback("Recommendation calculated successfully.");
    } catch (error) {
        showFeedback(error.message, true);
    } finally {
        button.disabled = false;
        button.textContent = "Recommend box →";
    }
});
