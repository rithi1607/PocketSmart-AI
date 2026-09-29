const $ = (selector) =>
    document.querySelector(selector);


async function api(url, options = {}) {

    const response = await fetch(
        url,
        {
            credentials: "same-origin",
            ...options
        }
    );


    let data = {};


    try {

        data = await response.json();

    } catch {

        data = {};

    }


    if (!response.ok) {

        throw new Error(
            data.detail ||
            "Request failed"
        );

    }


    return data;
}


function esc(value) {

    return String(
        value ?? ""
    ).replace(
        /[&<>'"]/g,
        character => ({
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            "'": "&#39;",
            '"': "&quot;"
        })[character]
    );
}


function renderResult(
    data,
    target = "#output"
) {

    const result =
        data.result || data;


    let html = `
        <div class="result-card">

            <h2>
                ${esc(
                    result.summary ||
                    "Recommendations"
                )}
            </h2>
    `;


    if (
        result.budget_allocation
    ) {

        html += `
            <h3>
                Budget allocation
            </h3>

            <div class="allocation">
        `;


        html += Object.entries(
            result.budget_allocation
        )
            .map(
                ([key, value]) => `
                    <span>
                        <b>
                            ${esc(key)}
                        </b>
                        <br>
                        ₹${Number(
                            value
                        ).toLocaleString(
                            "en-IN",
                            {
                                maximumFractionDigits: 0
                            }
                        )}
                    </span>
                `
            )
            .join("");


        html += `
            </div>
        `;
    }


    html += `
        <h3>
            Suggestions
        </h3>

        <div class="suggestions">
    `;


    html += (
        result.recommendations ||
        []
    )
        .map(item => {

            const amount =
                item.estimated_price ||
                item.estimated_total;


            return `
                <article>

                    <h3>
                        ${esc(
                            item.name ||
                            item.option ||
                            item.category
                        )}
                    </h3>

                    <p>
                        ${esc(
                            item.reason ||
                            item.match ||
                            ""
                        )}
                    </p>

                    <b>
                        ${
                            amount
                            ? "₹" +
                              Number(
                                  amount
                              ).toLocaleString(
                                  "en-IN",
                                  {
                                      maximumFractionDigits: 0
                                  }
                              )
                            : ""
                        }
                    </b>

                    <p class="muted">
                        ${esc(
                            item.platform ||
                            ""
                        )}
                    </p>

                </article>
            `;

        })
        .join("");


    html += `
        </div>
    `;


    if (result.tips) {

        html += `
            <h3>
                Tips
            </h3>

            <ul>
        `;


        html += result.tips
            .map(
                tip => `
                    <li>
                        ${esc(tip)}
                    </li>
                `
            )
            .join("");


        html += `
            </ul>
        `;
    }


    if (result.ai_note) {

        html += `
            <p class="notice">
                ${esc(
                    result.ai_note
                )}
            </p>
        `;
    }


    html += `
        </div>
    `;


    $(target).innerHTML =
        html;
}


function formJSON(form) {

    return Object.fromEntries(
        new FormData(form).entries()
    );
}


async function init() {

    const auth =
        $("#authLink");


    /*
     * Check login state
     */

    try {

        const session =
            await api(
                "/api/auth/session"
            );


        if (auth) {

            auth.textContent =
                "Logout";


            auth.href = "#";


            auth.onclick =
                async event => {

                    event.preventDefault();


                    await api(
                        "/api/auth/logout",
                        {
                            method: "POST"
                        }
                    );


                    location.href = "/";
                };
        }


        if ($("#welcome")) {

            $("#welcome").textContent =
                `Hi, ${session.user.name}`;
        }

    } catch {

        // User is not logged in
    }


    /*
     * Login
     */

    if ($("#loginForm")) {

        $("#loginForm").onsubmit =
            async event => {

                event.preventDefault();


                try {

                    await api(
                        "/api/auth/login",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify(
                                formJSON(
                                    event.target
                                )
                            )
                        }
                    );


                    location.href =
                        "/dashboard";

                } catch (error) {

                    $("#msg").textContent =
                        error.message;
                }
            };
    }


    /*
     * Register
     */

    if ($("#registerForm")) {

        $("#registerForm").onsubmit =
            async event => {

                event.preventDefault();


                try {

                    await api(
                        "/api/auth/register",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify(
                                formJSON(
                                    event.target
                                )
                            )
                        }
                    );


                    location.href =
                        "/dashboard";

                } catch (error) {

                    $("#msg").textContent =
                        error.message;
                }
            };
    }


    /*
     * Home Planner
     */

    if ($("#homeForm")) {

        $("#homeForm").onsubmit =
            async event => {

                event.preventDefault();


                try {

                    const form =
                        formJSON(
                            event.target
                        );


                    form.budget =
                        Number(
                            form.budget
                        );


                    form.items =
                        form.items
                            .split("\n")
                            .filter(
                                line =>
                                    line.trim()
                            )
                            .map(line => {

                                let [
                                    category,
                                    quantity = 1,
                                    notes = ""
                                ] =
                                    line
                                        .split("|")
                                        .map(
                                            value =>
                                                value.trim()
                                        );


                                return {
                                    category,
                                    quantity:
                                        Number(
                                            quantity
                                        ) || 1,
                                    notes
                                };

                            });


                    const result =
                        await api(
                            "/api/recommendations/home",
                            {
                                method: "POST",

                                headers: {
                                    "Content-Type":
                                        "application/json"
                                },

                                body: JSON.stringify(
                                    form
                                )
                            }
                        );


                    renderResult(result);

                } catch (error) {

                    $("#msg").textContent =
                        error.message;
                }
            };
    }


    /*
     * Party Planner
     */

    if ($("#partyForm")) {

        $("#partyForm").onsubmit =
            async event => {

                event.preventDefault();


                try {

                    const form =
                        formJSON(
                            event.target
                        );


                    form.budget =
                        Number(
                            form.budget
                        );


                    form.guests =
                        Number(
                            form.guests
                        );


                    const result =
                        await api(
                            "/api/recommendations/party",
                            {
                                method: "POST",

                                headers: {
                                    "Content-Type":
                                        "application/json"
                                },

                                body: JSON.stringify(
                                    form
                                )
                            }
                        );


                    renderResult(result);

                } catch (error) {

                    $("#msg").textContent =
                        error.message;
                }
            };
    }


    /*
     * Jewelry Planner
     */

    if ($("#jewelryForm")) {

        $("#jewelryForm").onsubmit =
            async event => {

                event.preventDefault();


                try {

                    const formData =
                        new FormData(
                            event.target
                        );


                    const result =
                        await api(
                            "/api/recommendations/jewelry",
                            {
                                method: "POST",
                                body: formData
                            }
                        );


                    renderResult(result);

                } catch (error) {

                    $("#msg").textContent =
                        error.message;
                }
            };
    }


    /*
     * History
     */

    if ($("#history")) {

        try {

            const rows =
                await api(
                    "/api/history"
                );


            if (rows.length) {

                $("#history").innerHTML =
                    rows
                        .map(
                            row => `
                                <a
                                    class="history-row"
                                    href="/history#${row.id}"
                                >

                                    <b>
                                        ${esc(
                                            row.planner
                                        )}
                                    </b>

                                    <span>
                                        ₹${Number(
                                            row.budget
                                        ).toLocaleString(
                                            "en-IN"
                                        )}
                                    </span>

                                    <span>
                                        ${new Date(
                                            row.created_at
                                        ).toLocaleString()}
                                    </span>

                                </a>
                            `
                        )
                        .join("");

            } else {

                $("#history").innerHTML =
                    "<p>No plans yet.</p>";
            }

        } catch (error) {

            $("#history").innerHTML =
                `<p>${esc(
                    error.message
                )}</p>`;
        }
    }


    /*
     * Recent dashboard plans
     */

    if ($("#recent")) {

        try {

            const rows =
                await api(
                    "/api/history"
                );


            $("#recent").innerHTML =
                rows
                    .slice(0, 5)
                    .map(
                        row => `
                            <div class="history-row">

                                <b>
                                    ${esc(
                                        row.planner
                                    )}
                                </b>

                                <span>
                                    ₹${Number(
                                        row.budget
                                    ).toLocaleString(
                                        "en-IN"
                                    )}
                                </span>

                            </div>
                        `
                    )
                    .join("")
                    ||
                    "<p>No plans yet.</p>";

        } catch {

            // Ignore dashboard history errors
        }
    }
}


document.addEventListener(
    "DOMContentLoaded",
    init
);